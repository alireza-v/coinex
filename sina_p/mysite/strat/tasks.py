from celery import shared_task
from tradingview_ta import TA_Handler,Interval
from time import sleep
from datetime import datetime
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

symbols=['BTCUSDT','BCHUSDT','ETHUSDT','1INCHUSDT','AAVEUSDT','ADAUSDT','ALGOUSDT','ANKRUSDT','APEUSDT','APTUSDT','ARUSDT','ATOMUSDT','AUDIOUSDT','AVAXUSDT','AXSUSDT','BATUSDT','BNBUSDT','BTTUSDT','CAKEUSDT','CELOUSDT','CHZUSDT','COMPUSDT','CRVUSDT','DASHUSDT','DOGEUSDT','DOTUSDT','DYDXUSDT','EGLDUSDT','ELONUSDT','ENJUSDT','ENSUSDT','EOSUSDT','ETCUSDT','FILUSDT','FLOWUSDT','FTMUSDT','GALAUSDT','GMTUSDT','GRTUSDT', 'HBARUSDT','HNTUSDT','HOTUSDT','ICPUSDT','ICXUSDT','IMXUSDT','IOSTUSDT','IOTAUSDT','IOTXUSDT','KAVAUSDT','KDAUSDT','KSMUSDT','LINKUSDT','LPTUSDT','LRCUSDT','LTCUSDT','LUNAUSDT','LUNCUSDT','MANAUSDT','MASKUSDT','MATICUSDT','MINAUSDT','MKRUSDT','NEARUSDT','NEOUSDT','NFTUSDT','OMGUSDT','ONEUSDT','ONTUSDT','QTUMUSDT','RENUSDT','RNDRUSDT','ROSEUSDT','RSRUSDT','RUNEUSDT','SANDUSDT','SCRTUSDT','SHIBUSDT','SKLUSDT','SNXUSDT','SOLUSDT','STORJUSDT','SUSHIUSDT','SXPUSDT','THETAUSDT','TRXUSDT','UNIUSDT','VETUSDT','WAVESUSDT','WAXPUSDT','WOOUSDT','XECUSDT','XLMUSDT','XMRUSDT','XRPUSDT','XTZUSDT','YFIUSDT','ZECUSDT','ZENUSDT','ZILUSDT','ZRXUSDT']

def current_time():
    start=datetime.timestamp(datetime.now())
    return start

def time_diff(old_time):
    now=datetime.timestamp(datetime.now())
    return now- old_time


@shared_task
def logic():
    handler=TA_Handler(
        symbol='',
        exchange='COINEX',
        screener='crypto',
        interval=Interval.INTERVAL_2_HOURS,
    )
    l={}
    while True:
        for x,y in enumerate(symbols):
            sleep(1)
            print('checking {}'.format(y))
            handler.symbol=y
            try:
                analysis=handler.get_analysis().indicators['change']
                if y in l.keys():
                    if time_diff(l.get(y))>7200:
                        l.pop(y)
                        print('{} popped out'.format(y))
                        sleep(2)

                elif y not in l.keys():
                    if analysis>=10:
                        l[y]=current_time()
                        print('{} ({:.2f}%) appended'.format(y,analysis))
                        message='>>>{} {:.2f}% <<<'.format(y,analysis)
                        send_mail(
                            'coinex future alarm',
                            message,
                            EMAIL_HOST_USER,
                            ['alirezasonym5@gmail.com','erfanvahdat.6@gmail.com'],
                            fail_silently=False,
                        )
                        sleep(2)
            except:
                print('exception')
                continue