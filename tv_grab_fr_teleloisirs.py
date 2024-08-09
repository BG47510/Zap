#!/usr/bin/python3

# 2020 auteur Mohamed El Morabity
# 2024 mise à jour BG47510


"""tv_grab_fr_teleloisirs.py - Grab French television listings using the Télé
Loisirs mobile API in XMLTV format.
"""

from argparse import ArgumentParser
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import functools
import logging
import re
import sys
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Union
import urllib.parse

from lxml.etree import Element  # type: ignore # nosec
from lxml.etree import ElementTree  # nosec # créer un document XML
from pytz.reference import LocalTimezone  # type: ignore
from requests import Response
from requests import Session
from requests.exceptions import RequestException


class TeleLoisirsException(Exception):
    """Classe de base pour les exceptions levées par le module."""


class TeleLoisirs:
    """Met en œuvre les fonctionnalités de saisie et de traitement nécessaires à la génération
    des données XMLTV de l’API mobile de Télé Loisirs.
    """

    _API_URL = "https://api-tel.programme-tv.net"
    _API_USER_AGENT = (
        "Tele-Loisirs(7.0.0|7000001) ~ Android(9|28) ~ "
        "mobile(xiaomi|Redmi_Note_8|density=2.75) ~ okhttp(4.8.0)"
    )
    _API_BROADCAST_PROJECTION = [
        "id",
        "startedAt",
        "soundFormat",
        "isMultiLanguage",
        "isVOST",
        "aspectRatio",
        "hasDeafSubtitles",
        "CSAAgeRestriction",
        "isHD",
        "isNew",
        "isRebroadcast",
        "channel{id}",
        "program{id}",
        "endedAt",
    ]
    _API_PROGRAM_PROJECTION = [
        "collectionItemPartIndex",
        "collectionItemTitle",
        "collectionItemIndex",
        "collectionItemPartCount",
        "title",
        "duration",
        "country",
        "releasedYear",
        "originalTitle",
        "isSilent",
        "isInColor",
        "rating",
        "collection{itemIndex,childCount,parentCollection{childCount}}",
        "formatGenre{format{title},genre{name}}",
        "image{height,urlTemplate,width}",
        "programProviderPeople{role,person{fullname},position}",
        "synopsis",
        "review",
        "_links{url}",
    ]
    _API_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    _API_XMLTV_CREDIT = {
        "Acteur": "actor",
        "Auteur": "writer",
        "Créateur": "writer",
        "Dialogue": "writer",
        "Guest Star": "guest",
        "Interprète": "actor",
        "Invité": "guest",
        "Mise en scène": "director",
        "Musique": "composer",
        "Présentateur": "presenter",
        "Réalisateur": "director",
        "Scénariste": "writer",
    }
    _API_ETSI_CATEGORIES = {
        "Ballet": "Music / Ballet / Dance",
        "Concert": "Music / Ballet / Dance",
        "Dessin animé": "Children's / Youth programmes",
        "Documentaire sportif": "Sports",
        "Documentaire": "News / Current affairs",
        "Emission sportive": "Sports",
        "Feuilleton": "Movie / Drama",
        "Film": "Movie / Drama",
        "Magazine sportif": "Sports",
        "Magazine": "Magazines / Reports / Documentary",
        "Opéra": "Music / Ballet / Dance",
        "Spectacle": "Show / Game show",
        "Série": "Movie / Drama",
        "Théâtre": "Arts / Culture (without music)",
        "Téléfilm": "Movie / Drama",
    }

    _XMLTV_DATETIME_FORMAT = "%Y%m%d%H%M%S %z"

    def __init__(
        self,
        generator: Optional[str] = None,
        generator_url: Optional[str] = None,
    ):
        self._generator = generator
        self._generator_url = generator_url

        self._session = Session()
        self._session.headers.update({"User-Agent": self._API_USER_AGENT})
        self._session.hooks = {"response": [self._requests_raise_status]}

        self._channels = self._get_channels()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._session:
            self._session.close()

    @staticmethod
    def _requests_raise_status(response: Response, *args, **kwargs) -> None:
        try:
            response.raise_for_status()
        except RequestException as ex:
            logging.debug(
                "Error while retrieving URL %s", response.request.url
            )
            try:
                raise TeleLoisirsException(
                    response.json().get("message") or ex
                )
            except ValueError:
                raise TeleLoisirsException(ex)

    def _query_api(
        self, path: str, **query: Union[int, str]
    ) -> Dict[str, Any]:
        url = "{}/{}".format(self._API_URL, path.strip("/"))
        response = self._session.get(url, params=query)

        logging.debug("Retrieved URL %s", response.request.url)

        data = response.json().get("data", {})

        # Paginated results
        if next_url := data.get("next"):
            parsed_url = urllib.parse.urlparse(next_url)
            query = dict(urllib.parse.parse_qs(parsed_url.query))
            data["items"] += self._query_api(parsed_url.path, **query).get(
                "items", []
            )

        return data

    @classmethod
    def _teleloisirs_to_xmltv_id(cls, channel_id: int) -> str:

        return f"{channel_id}.api-tel.programme-tv.net"

    @staticmethod
    def _get_icon_url(
        url_template: Optional[str],
        width: Optional[int],
        height: Optional[int],
    ) -> Optional[str]:
        if not url_template or not width or not height:
            return None

        return url_template.format(
            transformation="fit",
            width=width,
            height=height,
            parameters="_",
            title="image",
        )

    def _get_channels(self) -> Dict[str, Any]:
        channels = {}
        for package in self._query_api("v2/bouquets.json", limit="auto").get(
            "items", []
        ):
            for channel in package.get("channelBouquets", []):
                channel_data = channel.get("channel", {})
                channel_id = channel_data.get("id")
                channel_name = channel_data.get("title")
                if not channel_id or not channel_name:
                    continue
                image = channel_data.get("image", {})
                channels[self._teleloisirs_to_xmltv_id(channel_id)] = {
                    "id": channel_id,
                    "display-name": channel_name,
                    "icon": {
                        "src": self._get_icon_url(
                            image.get("urlTemplate"),
                            image.get("width"),
                            image.get("height"),
                        ),
                        "width": image.get("width"),
                        "height": image.get("height"),
                    },
                    "url": channel_data.get("_links", {}).get("url"),
                }

        return channels

    def get_available_channels(self) -> Dict[str, str]:
        """Retourne la liste de toutes les chaînes disponibles sur Télé Loisirs, avec
        son identifiant XMLTV et son nom.
        """

        return {k: v["display-name"] for k, v in self._channels.items()}

    @staticmethod
    def _to_string(value: Union[None, bool, int, str]) -> Optional[str]:
        if isinstance(value, bool):
            return "yes" if value else "no"

        if value:
            stripped_value = str(value).strip()

        if not value or not stripped_value:
            return None

        return stripped_value

    @staticmethod
    def _xmltv_element(
        tag: str,
        text: Union[None, int, str] = None,
        parent: Element = None,
        **attributes: Union[None, int, str],
    ) -> Element:
        attributes = {
            k: w
            for k, v in attributes.items()
            if (w := TeleLoisirs._to_string(v))
        }

        element = Element(tag, **attributes)
        element.text = TeleLoisirs._to_string(text)

        if parent is not None:
            parent.append(element)

        return element

    @staticmethod
    def _xmltv_element_with_text(
        tag: str,
        text: Union[None, int, str],
        parent: Element = None,
        **attributes: Optional[str],
    ) -> Optional[Element]:
        if not TeleLoisirs._to_string(text):
            return None

        return TeleLoisirs._xmltv_element(
            tag, text=text, parent=parent, **attributes
        )

    def _to_xmltv_channel(self, channel_id: str) -> Optional[Element]:
        xmltv_channel = Element("channel", id=channel_id)

        channel_data = self._channels.get(channel_id)
        if not channel_data:
            return None

        # Nom d’affichage de la chaîne
        self._xmltv_element_with_text(
            "display-name",
            channel_data.get("display-name"),
            parent=xmltv_channel,
        )

        # Icône associée au programme
        self._xmltv_element(
            "icon", parent=xmltv_channel, **channel_data.get("icon", {})
        )

        # URL pour en savoir plus sur la chaîne
        self._xmltv_element_with_text(
            "url", channel_data.get("url"), parent=xmltv_channel
        )

        return xmltv_channel

    @staticmethod
    # pylint: disable=too-many-arguments
    def _get_xmltv_ns_episode_number(
        season: Optional[int],
        total_seasons: Optional[int],
        episode: Optional[int],
        total_episodes: Optional[int],
        part: Optional[int],
        total_parts: Optional[int],
    ) -> Optional[str]:
        if not season and not episode and not part:
            return None

        result = ""

        if season:
            result = f"{season - 1}"
            if total_seasons:
                result += f"/{total_seasons}"

        result += "."

        if episode:
            result += f"{episode - 1}"
            if total_episodes:
                result += f"/{total_episodes}"

        result += "."

        if not part:
            part = 1
        if not total_parts:
            total_parts = 1

        if part:
            result += f"{part - 1}"
            if total_parts:
                result += f"/{total_parts}"

        return result

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    def _to_xmltv_program(
        self, broadcast: Dict[str, Any], program: Dict[str, Any]
    ) -> Optional[Element]:
        broadcast_id = broadcast.get("id")

        # ID de la chaîne
        channel_id = self._teleloisirs_to_xmltv_id(
            broadcast.get("channel", {}).get("id")
        )
        if not channel_id:
            logging.debug(
                "Broadcast %s has no channel ID, skipping", broadcast_id
            )
            return None

        # Heure de début
        try:
            start = datetime.strptime(
                broadcast.get("startedAt", ""), self._API_DATETIME_FORMAT,
            ).strftime(self._XMLTV_DATETIME_FORMAT)
        except ValueError:
            logging.debug(
                "Broadcast %s has no valid start time, skipping", broadcast_id,
            )
            return None

        # Heure de fin
        stop = None
        try:
            stop = datetime.strptime(
                broadcast.get("endedAt", ""), self._API_DATETIME_FORMAT
            ).strftime(self._XMLTV_DATETIME_FORMAT)
        except ValueError:
            pass

        xmltv_program = self._xmltv_element(
            "programme", start=start, stop=stop, channel=channel_id
        )

        # Titre du programme
        title = program.get("title") or program.get("collectionItemTitle")
        xmltv_title = self._xmltv_element_with_text(
            "title", title, parent=xmltv_program
        )
        if xmltv_title is None:
            logging.warning(
                "Program %s has no title, skipping", broadcast.get("id")
            )
            return None

        if original_title := program.get("originalTitle"):
            xmltv_title.set("lang", "fr")
            self._xmltv_element_with_text(
                "title", original_title, parent=xmltv_program
            )

        # Sous-titre ou titre de l’épisode
        if title != (item_title := program.get("collectionItemTitle")):
            self._xmltv_element_with_text(
                "sub-title", item_title, parent=xmltv_program
            )

        # Description de l’émission ou de l’épisode
        self._xmltv_element_with_text(
            "desc", program.get("synopsis"), parent=xmltv_program
        )

        # Crédits du programme
        xmltv_credits = self._xmltv_element("credits")
        _credits = {
            "director": {},
            "actor": {},
            "writer": {},
            "adapter": {},
            "producer": {},
            "composer": {},
            "editor": {},
            "presenter": {},
            "commentator": {},
            "guest": {},
        }  # type: Dict[str, Dict[str, Element]]

        for people in program.get("programProviderPeople", []):
            position = people.get("position")
            credit = self._API_XMLTV_CREDIT.get(position)
            if not credit:
                if position:
                    logging.debug(
                        'No XMLTV credit defined for function "%s"', position,
                    )
                continue

            if full_name := people.get("person", {}).get("fullname"):
                _credits[credit][full_name] = self._xmltv_element_with_text(
                    credit,
                    full_name,
                    role=people.get("role") if credit == "actor" else None,
                )

        xmltv_credits.extend(
            [e for s in _credits.values() for e in s.values()]
        )
        if len(xmltv_credits) > 0:
            xmltv_program.append(xmltv_credits)

        # Date à laquelle l’émission ou le film a été terminé
        self._xmltv_element_with_text(
            "date", program.get("releasedYear"), parent=xmltv_program,
        )

        # Type de programme
        genres = program.get("formatGenre", {})
        genre = genres.get("format", {}).get("title", "").capitalize()
        self._xmltv_element_with_text(
            "category", genre, parent=xmltv_program, lang="fr",
        )
        if genre != (
            sub_genre := genres.get("genre", {}).get("name", "").capitalize()
        ):
            self._xmltv_element_with_text(
                "category", sub_genre, parent=xmltv_program, lang="fr",
            )
        etsi_category = self._API_ETSI_CATEGORIES.get(genre)
        self._xmltv_element_with_text(
            "category", etsi_category, parent=xmltv_program, lang="en",
        )
        if genre and not etsi_category:
            logging.debug('No ETSI category found for genre "%s"', genre)

        # Durée réelle du programme
        self._xmltv_element_with_text(
            "length",
            program.get("duration"),
            parent=xmltv_program,
            units="seconds",
        )

        # Icône associée au programme
        image = program.get("image") or {}
        if url_template := image.get("urlTemplate"):
            self._xmltv_element(
                "icon",
                parent=xmltv_program,
                src=self._get_icon_url(
                    url_template, image.get("width"), image.get("height"),
                ),
                width=image.get("width"),
                height=image.get("height"),
            )

        # URL où vous pouvez en savoir plus sur le programme
        self._xmltv_element_with_text(
            "url", program.get("_links", {}).get("url"), parent=xmltv_program,
        )

        # Pays où le programme a été réalisé ou l’un des pays
        # production conjointe
        if countries := program.get("country", ""):
            for country in countries.split(" - "):
                self._xmltv_element_with_text(
                    "country", country, parent=xmltv_program, lang="fr",
                )

        # Numéro de l’épisode
        collection = program.get("collection") or {}
        self._xmltv_element_with_text(
            "episode-num",
            self._get_xmltv_ns_episode_number(
                collection.get("itemIndex"),
                (collection.get("parentCollection") or {}).get("childCount"),
                program.get("collectionItemIndex"),
                collection.get("childCount"),
                program.get("collectionItemPartIndex"),
                program.get("collectionItemPartCount"),
            ),
            parent=xmltv_program,
            system="xmltv_ns",
        )

        # Détails de la vidéo
        xmltv_video = self._xmltv_element("video", parent=xmltv_program)
        self._xmltv_element_with_text("present", True, parent=xmltv_video)
        self._xmltv_element_with_text(
            "colour", program.get("isInColor"), parent=xmltv_video
        )
        self._xmltv_element_with_text(
            "aspect", broadcast.get("aspectRatio"), parent=xmltv_video
        )
        if broadcast.get("isHD"):
            self._xmltv_element_with_text(
                "quality", "HDTV", parent=xmltv_video
            )

        # Détails audio
        xmltv_audio = self._xmltv_element("audio")
        if program.get("isSilent"):
            self._xmltv_element("present", False, parent=xmltv_audio)
        elif stereo := (
            "bilingual"
            if broadcast.get("isMultiLanguage")
            else broadcast.get("soundFormat")
        ):
            self._xmltv_element("present", True, parent=xmltv_audio)
            self._xmltv_element("stereo", stereo, parent=xmltv_audio)
        if xmltv_audio is not None:
            xmltv_program.append(xmltv_audio)

        # Programme déjà montré ?
        if broadcast.get("isRebroadcast"):
            self._xmltv_element(
                "previously-shown", parent=xmltv_program,
            )
        # Programme en avant-première ?
        elif broadcast.get("isNew"):
            self._xmltv_element("premiere", parent=xmltv_program)

        # Sous-titres
        if broadcast.get("hasDeafSubtitles"):
            self._xmltv_element(
                "subtitles", parent=xmltv_program, type="deaf-signed"
            )
        if broadcast.get("isVOST"):
            self._xmltv_element(
                "subtitles", parent=xmltv_program, type="onscreen"
            )

        # Notation
        if csa_age_restriction := broadcast.get("CSAAgeRestriction"):
            self._xmltv_element_with_text(
                "value",
                f"Interdit aux moins de {csa_age_restriction} ans",
                parent=self._xmltv_element(
                    "rating", parent=xmltv_program, system="CSA"
                ),
            )

        # Étoiles
        if rating := int((program.get("rating") or 0) * 4):
            self._xmltv_element_with_text(
                "value",
                f"{rating}/4",
                parent=self._xmltv_element(
                    "star-rating", parent=xmltv_program, system="Télé Loisirs"
                ),
            )

        # Revoir
        self._xmltv_element_with_text(
            "review",
            program.get("review"),
            parent=xmltv_program,
            type="text",
            source="Télé Loisirs",
            lang="fr",
        )

        return xmltv_program

    def _get_xmltv_programs(
        self, channel_ids: List[str], days: int, offset: int
    ) -> Generator[Element, None, None]:

        start = datetime.combine(
            date.today(), time(0), tzinfo=LocalTimezone()
        ) + timedelta(days=offset)
        end = start + timedelta(days=days)

        teleloisirs_channel_ids = [
            str(channel_id)
            for c in channel_ids
            if (channel_id := self._channels.get(c, {}).get("id"))
        ]

        # Utiliser le dictionnaire pour éviter les doublons de diffusion
        broadcasts = {
            i: b
            for b in self._query_api(
                "v2/broadcasts.json",
                channels=",".join(teleloisirs_channel_ids),
                limit="auto",
                projection=",".join(self._API_BROADCAST_PROJECTION),
                since=start.strftime(self._API_DATETIME_FORMAT),
                until=end.strftime(self._API_DATETIME_FORMAT),
            ).get("items", [])
            if (i := b.get("id"))
        }

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    functools.partial(
                        self._query_api,
                        projection=",".join(self._API_PROGRAM_PROJECTION),
                    ),
                    "v2/programs/{}.json".format(
                        b.get("program", {}).get("id")
                    ),
                )
                for b in broadcasts.values()
            ]

            for broadcast, future in zip(broadcasts.values(), futures):
                program = future.result().get("item", {})
                yield self._to_xmltv_program(broadcast, program)

    def _to_xmltv(
        self, channel_ids: List[str], days: int, offset: int
    ) -> ElementTree:
        xmltv = self._xmltv_element(
            "tv",
            **{
                "source-info-name": "Télé Loisirs",
                "source-info-url": "https://www.programme-tv.net/",
                "source-data-url": self._API_URL,
                "generator-info-name": self._generator,
                "generator-info-url": self._generator_url,
            },
        )

        xmltv_channels = {}  # type: Dict[str, Element]
        xmltv_programs = []

        for xmltv_program in self._get_xmltv_programs(
            channel_ids, days, offset
        ):
            if xmltv_program is None:
                continue
            channel_id = xmltv_program.get("channel")
            if channel_id not in xmltv_channels:
                xmltv_channels[channel_id] = self._to_xmltv_channel(channel_id)
            xmltv_programs.append(xmltv_program)

        xmltv.extend(xmltv_channels.values())
        xmltv.extend(xmltv_programs)

        return ElementTree(xmltv)

    def write_xmltv(
        self, channel_ids: List[str], output_file: Path, days: int, offset: int
    ) -> None:
        """Prenez les émissions de Télé Loisirs en format XMLTV et écrivez-les à
        file.
        """

        logging.debug("Writing XMLTV program to file %s", output_file)

        xmltv_data = self._to_xmltv(channel_ids, days, offset)
        xmltv_data.write(
            str(output_file),
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
        )


_PROGRAM = "tv_grab_fr_teleloisirs"
__version__ = "1.0"
__url__ = "https://github.com/BG47510/epg/tv_grab_fr_teleloisirs"

_DESCRIPTION = "France (Télé Loisirs)"
_CAPABILITIES = ["baseline", "manualconfig"]

_DEFAULT_DAYS = 1
_DEFAULT_OFFSET = 0

_DEFAULT_CONFIG_FILE = Path.home().joinpath(".xmltv", f"{_PROGRAM}.conf")


def _print_description() -> None:
    print(_DESCRIPTION)


def _print_version() -> None:
    print("This is {} version {}".format(_PROGRAM, __version__))


def _print_capabilities() -> None:
    print("\n".join(_CAPABILITIES))


def _parse_cli_args() -> Namespace:
    parser = ArgumentParser(
        description="Obtenir les programmes de la télévision française avec Télé Loisirs mobile."
        "API au format XMLTV"
    )
    parser.add_argument(
        "--description",
        action="store_true",
        help="Imprimer la description de cet exécuteur",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Voir la version de cet exdcuteur",
    )
    parser.add_argument(
        "--capabilities",
        action="store_true",
        help="Montrez les capacités prises en charge par cette carte d’acquisition",
    )
    parser.add_argument(
        "--configure",
        action="store_true",
        help="Générez le fichier de configuration en demandant aux utilisateurs"
        "channels to grab",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=_DEFAULT_DAYS,
        help="Accumulez des jours de données TV (default: %(default)s)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=_DEFAULT_OFFSET,
        help="Récupérer les données TV à partir des jours OFFSET à l’avenir (default: "
        "%(default)s)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/dev/stdout"),
        help="écrire les données XML dans OUTPUT au lieu de la sortie standard",
    )
    parser.add_argument(
        "--config-file",
        type=Path,
        default=_DEFAULT_CONFIG_FILE,
        help="nom de fichier pour écrire/charger la configuration vers/depuis (default: "
        "%(default)s)",
    )

    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument(
        "--quiet",
        action="store_true",
        help="n’affiche que les messages d’erreur sur STDERR",
    )
    log_level_group.add_argument(
        "--debug",
        action="store_true",
        help="Fournir plus d’informations sur les progrès réalisés à l’égard de la stratégie pour aider au"
        "débogage",
    )

    return parser.parse_args()


def _read_configuration(
    available_channels: Dict[str, str], config_file: Path
) -> List[str]:

    channel_ids = set()
    with config_file.open("r") as config_reader:
        for line in config_reader:
            match = re.search(r"^\s*channel\s*=\s*(.+)\s*$", line)
            if match is None:
                continue

            channel_id = match.group(1)
            if channel_id in available_channels:
                channel_ids.add(channel_id)

    return list(channel_ids)


def _write_configuration(channel_ids: List[str], config_file: Path) -> None:

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, "w") as config:
        for channel_id in channel_ids:
            print("channel={}".format(channel_id), file=config)


def _configure(available_channels: Dict[str, str], config_file: Path) -> None:
    channel_ids = []
    answers = ["yes", "no", "all", "none"]
    select_all = False
    select_none = False
    print(
        "Sélectionnez les chaînes pour lesquelles vous souhaitez recevoir des données.",
        file=sys.stderr,
    )
    for channel_id, channel_name in available_channels.items():
        if not select_all and not select_none:
            while True:
                prompt = f"{channel_name} [{answers} (default=no)] "
                answer = input(prompt).strip()  # nosec
                if answer in answers or answer == "":
                    break
                print(
                    f"invalid response, please choose one of {answers}",
                    file=sys.stderr,
                )
            select_all = answer == "all"
            select_none = answer == "none"
        if select_all or answer == "yes":
            channel_ids.append(channel_id)
        if select_all:
            print(f"{channel_name} yes", file=sys.stderr)
        elif select_none:
            print(f"{channel_name} no", file=sys.stderr)

    _write_configuration(channel_ids, config_file)


def _main() -> None:
    args = _parse_cli_args()

    if args.version:
        _print_version()
        sys.exit()

    if args.description:
        _print_description()
        sys.exit()

    if args.capabilities:
        _print_capabilities()
        sys.exit()

    logging_level = logging.INFO
    if args.quiet:
        logging_level = logging.ERROR
    elif args.debug:
        logging_level = logging.DEBUG
    logging.basicConfig(
        level=logging_level, format="%(levelname)s: %(message)s",
    )

    try:
        tele_loisirs = TeleLoisirs(generator=_PROGRAM, generator_url=__url__)
    except TeleLoisirsException as ex:
        logging.error(ex)
        sys.exit(1)

    logging.info("Using configuration file %s", args.config_file)

    available_channels = tele_loisirs.get_available_channels()
    if args.configure:
        _configure(available_channels, args.config_file)
        sys.exit()

    if not args.config_file.is_file():
        logging.error(
            "Vous devez configurer la carte de saisie en l’exécutant avec --configure"
        )
        sys.exit(1)

    channel_ids = _read_configuration(available_channels, args.config_file)
    if not channel_ids:
        logging.error(
            "Le fichier de configuration %s est vide ou mal formé, supprimez et exécutez avec"
            "--configure",
            args.config_file,
        )
        sys.exit(1)

    try:
        tele_loisirs.write_xmltv(
            channel_ids, args.output, days=args.days, offset=args.offset
        )
    except TeleLoisirsException as ex:
        logging.error(ex)


if __name__ == "__main__":
    _main()
