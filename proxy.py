from Logger import logger


proxy_list = [
    {
        "proxyHost": "http-proxy-sg2.dobel.cn",
        "proxyPort": "9180",
        "proxyUser": "ZYYTHTT1",
        "proxyPass": "6tEQ26bA9"
    },
    {
        "proxyHost": "http-proxy-sg2.dobel.cn",
        "proxyPort": "9180",
        "proxyUser": "DONGNANHTT1",
        "proxyPass": "T74B13bQ"
    }
]


def proxy_cfg():
    proxy_id = int(input('input proxy id: '))
    r_proxy = None
    if proxy_id in range(len(proxy_list)):
        proxy_info = proxy_list[proxy_id]
        proxyHost = proxy_info['proxyHost']
        if proxyHost == "proxy.crawlera.com":
            proxyPort = proxy_info['proxyPort']
            proxyAuth = proxy_info['proxyAuth']
            logger.info('proxy: %s is chosen!\n' % proxyHost)
            r_proxy = {"https": "https://{}@{}:{}/".format(proxyAuth, proxyHost, proxyPort),
                       "http": "http://{}@{}:{}/".format(proxyAuth, proxyHost, proxyPort)}
            return r_proxy
        proxyPort = proxy_info['proxyPort']
        proxyUser = proxy_info['proxyUser']
        proxyPass = proxy_info['proxyPass']
        logger.info('proxy: %s is chosen!\n' % proxyUser)
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        r_proxy = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
    else:
        logger.info('proxy is None!')
    return r_proxy

if __name__ == '__main__':
    p = proxy_cfg()
    print(p)
