
FRECUENCIA_MINUTOS=15
MAIN_SLEEP_TIME=900    # 60 * FRECUENCIA_MINUTOS

SPLIT=10
TIMEOUT=10
PriceOverlap=0.0015

MinOrderAsset=0.1
MinOrderCurr=0.0001


API_KEY='BQDLO5T5-3LRJEACQ-E6NF99LR-V4WZXDTY'
API_SECRET='392d25a3059ecfe0fded3c11e8b92c0eafafc512d241000a960ea96545e7bb55c5cf6d65afafcf0fe7a9c2b9dbb175dad1956029a8b798c6564195d20cdc5008'


# ////////////////////////////////////
# CONSTANTES ZF4 ANG
# ////////////////////////////////////

ALGO="ZF4 ANG"

PAIR='BTC_ETH'
PairAsset='ETH'
PairCurr='BTC'

A1	=  -6.68
B1	=  -9.87
C1	=   25.41
D1	=  -36.95

LRp1	=  307
LRp2	=  270
LRp3	=  115
LRp4	=  112

STDp1	= 425
STDp2	= 232
STDp3	=  94
STDp4	= 373

ap      = 378
au      =  12.35
ad      =-6.51

FL1	= -24.82
FL2	=  87.69
FL3	=   5.73
FL4	= -21.26

Th1     =  12.185
Th2     =  -6.277

# ////////////////////////////////////
# CONSTANTES ZF4 LogK(c)
# ////////////////////////////////////

#ALGO="ZF4"

#BASE=303.7 #No lo estoy usando ahora
#A1=-27.6
#B1=-58.1
#C1= 74.2
#D1= 12.5
#LRp1=1144
#LRp2=1563
#LRp3=1123
#LRp4=444
#STDp1=1388
#STDp2=1053
#STDp3=1594
#STDp4=274
#FL1=-20.8
#FL2= 16.7
#FL3=-12.5
#FL4= 21.4

#Th1= 36.08
#Th2=-39.57




# ////////////////////////////////////
# CONSTANTES PUCK II
# ////////////////////////////////////

#ALGO="P3F2"

#BASE = 377.43

#P1=  35
#S1=  221
#P2=  381
#S2=  214
#K1=-57.937
#K2= 194.266
#ThL= -0.478
#ThS=  -0.216

#Fo1= 495
#Fo2= 145
#FT =  0.051
#Cr1= 24
#Cr2= 4
#CT =  0




#VELAS

NUMVELAS=500
DELAY=0

HISTVELAS=8760


# start gui
gui = False

# candles chart time
BARS_TIME = "60"

# broker data refresh thread sleep time 
BROKER_SLEEP_TIME =9 

# main algorithm loop sleep time
MAIN_SLEEP_TIME = 35

# assets on which this script trades
SYMBOLS = ["EURUSD"]
# all symbols:
#BTCUSD, EURCHF, USDCAD, GBPUSD, EURGBP, EURJPY, EURNOK, EURSEK, EURUSD, NZDUSD, USDCNH, AUDNZD, AUDUSD, USDRUB, USDJPY, USDCHF, SILVER, GOLD, OILWTI, NFLX, MSFT, PEP, WU, TSLA, TWTR, BAC, V, VOW, KO, AAPL, BMW, BABA, F, FB, GOOG, GPRO, AMZN, INTC, CSCO, AU200, CH30, DAX, UK100, DOW, EU50, SP500, HK50, JP225

# margin used for single position, and leverage
MARGIN = "0.20"
LEVERAGE = "10"

# stop loss&take profit; in market change, multiply by leverage to get profit or loss %
# divided by leverage to get pure %
STOP_LOSS_PERCENT = 0
# round(0.75/float(LEVERAGE), 2)
TAKE_PROFIT_PERCENT = 0 
#round(1.5/float(LEVERAGE), 2)

# your 1broker API token
API_KEY = "8f42c96ed285f57fb608a4885c17ef05"

# old, trailing stop setting
FOLLOWING_STOP_MARGIN = 2000

running = True

STARTING_HIGHEST_PL = -FOLLOWING_STOP_MARGIN
current_position_highest_profitloss = STARTING_HIGHEST_PL


vZF4=0
TrendingUp=False
TrendingDn=False
sig=0
ticker=0
price=0



# 1broker
overview = ""
bars = {}
position = {}
orders = False
profitloss = 0
balance = 0
locked_balance = 0
total_btc = 0
sma5 = {}
sma20 = {}
prev_sma5 = {}
prev_sma20 = {}

# some stats
broker_fetch_count = 0
startup_balance = 0

# init
for symbol in SYMBOLS:
	sma5[symbol] = 0
	sma20[symbol] = 0
	prev_sma5[symbol] = 0
	prev_sma20[symbol] = 0
	position[symbol] = (False, False)

# logging
import logging
import logging.config
log_level = "DEBUG"
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': log_level,
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': "DEBUG",
            'filename': 'debug.log',
            'maxBytes': 2097152, # 2 MiB
            'backupCount': 10,
        },
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': "INFO",
            'filename': 'info.log',
            'maxBytes': 2097152, # 2 MiB
            'backupCount': 10,
        }
    },
    'loggers': {
        'console_only': {
            'handlers': ['console'],
            'propagate' : 0
        },
        'file_only': {
            'handlers': ['file'],
            'propagate' : 0
        },
        'both': {
            'handlers': ['console', 'file'],
            'propagate' : 0
        },
    },
    'root': {
        'level': log_level,
        'handlers': ['console', 'file', 'file_info'],
    },
})
