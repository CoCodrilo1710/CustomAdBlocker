# CustomAdBlocker
Custom DNS Ad Blocker

## Instructions & Docs

In order to get this app fully functional you need to set a custom DNS to your home network.
The IP will be 127.0.0.1

Help with finding where you can set a custom server:

( Windows and MAC ): https://www.hellotech.com/guide/for/how-to-change-dns-server-windows-mac

( linux ) : https://www.linuxfordevices.com/tutorials/linux/change-dns-on-linux

The app is working by querying a given file full of known spam domains with the AAAA domain located in the DNS request to out custom server.
After analyzing the requested domain, the server will answear with either 0.0.0.0 as blocked domain ( found in the given dictionary ) or the correct ip associated with the domain ( after sending a request to Google DNS ) ( if not found in the dictionary ).
