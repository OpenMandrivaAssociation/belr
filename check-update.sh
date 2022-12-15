#!/bin/sh
#curl -s "https://github.com/BelledonneCommunications/belr/tags" |grep "tag/" |sed -e 's,.*tag/,,;s,\".*,,;' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1
curl -s "https://gitlab.linphone.org/BC/public/belr/-/tags" |grep "tags/" |sed -e 's,.*tags/,,;s,\".*,,;' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1

