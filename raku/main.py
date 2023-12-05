#!/usr/bin/env python3

import sys
from typing import List
import rakuten


def generate_list(channels: List[rakuten.Channel]) -> None:
    list_builder = []
    
    list_builder.append("#EXTM3U")

    # get streams
    ch_streams = rakuten.map_channels_streams(channels)
    
    head_line_format = "#EXTINF:-1 tvg-chno={} tvg-id=\"{}\" tvg-name=\"{}\" group-title=\"{}\",{}"
    
    for ch in sorted(channels, key=lambda x: x.channel_number):
        head_line = head_line_format.format(
            ch.numerical_id,
            ch.id,
            ch.title,
            ch.category.lower(),
            ch.title,
        )

        list_builder.append(head_line)
        list_builder.append(ch_streams.get(ch.id, "# no_stream"))
    
    return "\n".join(list_builder)
     

def main():
    channels = rakuten.get_channels()
    m3u_list = generate_list(channels)
    #print(m3u_list)
    with open("rakuten.m3u", "wb") as fp:
        fp.write(m3u_list.encode())


if __name__ == "__main__":
    sys.exit(main())
