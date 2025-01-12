""" Only update cloudns when our IP address actually changes, to be nice """

import os
import sys
from time import sleep
from requests import get


def get_public_ip():
    """Retrieve external ip address"""
    print("Retrieving external IP address")
    ip = get("https://api.ipify.org",timeout=20).content.decode("utf8")
    return ip


def block(interval):
    """Block until we can access the internet"""
    debug = False
    test_ip = "0.0.0.0"  # This should exist, and dns not required to interpret it
    while True:

        try:
            response = os.system("ping -c 1 -w2 " + test_ip + " > /dev/null 2>&1")
            if response == 0:
                return
            if debug:
                print(test_ip, "ignoring pings")
        except Exception as err:
            if debug:
                print(err)
        sleep(interval)


def update_ip(old_ip, dynamic_dns_url):
    """This is the cloudns defined magic url trick to ask them to update"""
    test = False

    if not test:
        try:
            if sys.version_info[0] < 3:
                import urllib

                page = urllib.urlopen(dynamic_dns_url)
                page.close()
            else:
                import urllib.request

                page = urllib.request.urlopen(dynamic_dns_url)
                page.close()
        except:
            return False
    else:
        print("Dummy call to update IP")

    # Check request to change ip dns worked

    new_ip = get_public_ip()

    if new_ip != old_ip:
        return True

    return False


def initialise_ip_file(ipfilename):
    """If we haven't got an ip file, create a dummy one"""
    try:
        ipfile = open(ipfilename, "r", encoding="ascii")
    except FileNotFoundError:
        ipfile = open(ipfilename, "w", encoding="ascii")
        ipfile.write("no ip")

    ipfile.close()


def read_ip_file(ipfilename):
    """Read file containing what we last found our ip to be"""
    with open(ipfilename, "r", encoding="ascii") as ipfile:
        pubip = ipfile.readline()
    return pubip


def update_ip_file(ip, ipfilename):
    """Write file recording what our ip was"""

    with open(ipfilename, "w", encoding="ascii") as ipfile:
        ipfile.write(ip)


def update_dns(dynamic_dns_url):
    """Make dns match our current ip"""

    # This file contains our current understanding of what our ip is

    ipfilename = "/tmp/ipfile.txt"
    initialise_ip_file(ipfilename)
    old_ip = read_ip_file(ipfilename)

    # If we find we haven't got internet access, wait until we do,
    # At least for 28 minutes, when we try again soon anyway

    block(28)

    ip = get_public_ip()

    if old_ip != ip:
        print("ip changed, update ip file")
        if update_ip(old_ip, dynamic_dns_url):
            update_ip_file(ip, ipfilename)
    else:
        print("Ip unchanged, quit")
        sys.exit()

    print("New IP: " + str(ip))


def main():
    """The url we need to look at to update our ip is passed as an argument"""
    inputargs = sys.argv
    sys.argv.pop(0)

    if len(inputargs) != 1:
        print("Error, Usage : dynamic_cloudns.py dynamic_dns_url")
        sys.exit()

    dynamic_dns_url = inputargs[0]
    update_dns(dynamic_dns_url)


if __name__ == "__main__":
    main()
