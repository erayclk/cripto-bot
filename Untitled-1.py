from formulas import *
import time
from binance import Client
from decimal import Decimal
import threading

api_key = ''
api_secret = ''

kaldıraç = 20
miktar = 13
emir_noktası = 1.3

sembol = 'ALGOUSDT'

tetikleyici = True #True ise fiyat emir noktasına ulaştığında alış emri verir, değilse normal sürecine devam eder

bölgeler = [[2800,2700]] #İki bölge tanımlandı

#Sabit Deklarasyonlar
canlı_fiyat = 0
saat_hızı = .2
bölgenin_içinde = False
uzun_pozisyon_acık = False
kısa_pozisyon_acık = False
başlangıç = False

#Kar Sistemleri
ara_emir_noktası = emir_noktası
izleyen_uzun_hedef = 5
izleyen_uzun_baz = 3

izleyen_uzun_değişim = izleyen_uzun_hedef - izleyen_uzun_baz

izleyen_kısa_hedef = 5
izleyen_kısa_baz = 3

izleyen_kısa_değişim = izleyen_kısa_hedef - izleyen_kısa_baz

uzun_emir_noktası_değişti = False
kısa_emir_noktası_değişti = False

#Sabit Deklarasyonlar Sonu

#Binance Sunucusuna Bağlanma
print("Binance Sunucusuna Bağlanılıyor")
client = Client(api_key,api_secret)
print("Bağlantı Başarılı")
#Bağlantı Tamam

#Kar izleme mekanizması
def target_chaser():
    global intermediate_order_point
    
    global order_point
    global live_price
    global lever

    global trailing_long_target
    global trailing_long_base

    global trailing_short_target
    global trailing_short_base

    global position_long_open
    global position_short_open
    
    global trailing_long_shift
    global trailing_short_shift
    
    while True:

        kar = abs(oranli_kar(intermediate_order_point,live_price,lever))
        
        print(f'{intermediate_order_point} ve {live_price} fiyatları için {lever} kaldıraç oranı ile elde edilen kar oranı: {kar}')


        if position_long_open and kar >= 1:
            print(f"Uzun pozisyondan sağlanan kaldıraçlı kar oranı: {kar}")
        if position_short_open and kar >= 1:
            print(f"Kısa pozisyondan sağlanan kaldıraçlı kar oranı: {kar}")

        if position_long_open and kar > trailing_long_target and kar == (trailing_long_target + trailing_long_shift): # Fiyat Kar Hedefine Ulaştı
            
            trailing_long_target = trailing_long_target + trailing_long_shift
            trailing_long_base = trailing_long_base + trailing_long_shift
            
            print(f"Kâr hedefi değişti, güncel {trailing_long_target} ve kesme noktası {trailing_long_base}")
            
        if position_short_open and kar > trailing_short_target and kar == (trailing_short_target + trailing_short_shift):
            
            trailing_short_target = trailing_short_target + trailing_short_shift
            trailing_short_base = trailing_short_base + trailing_short_shift
            
            print(f"Kâr hedefi değişti, güncel {trailing_short_target} ve kesme noktası {trailing_short_base}")
def CloseOrder(Tip:str):
    global ticker
    global lever
    global quant
    orderBuy = client.futures_change_leverage(symbol=ticker, leverage=lever)
   
    #pozisyonu kapatmak için emir tipini tersine çevirme
    if Tip == 'ALIM':
       Tip = 'SATIŞ'
    else:
       Tip = 'ALIM'
    try:
       print(client.futures_create_order(
       symbol=ticker,
       type='MARKET',
       side=Tip,
       quantity=quant,
       reduceOnly=True))
       print(Tip+" başarıyla kapatıldı.")
    #Reduce Only, bu işlemin yeni bir işlem açmamasını ve yalnızca mevcut işlemi kapatmasını sağlar
    except:
       print(Tip+" işlemi kapatılamadı.")
def CloseOrder(tip:str):
    global ticker
    global kaldıraç
    global miktar
    emirAl = client.futures_change_leverage(symbol=ticker, leverage=kaldıraç)
   
    #pozisyonu kapatmak için emir tipini tersine çevirme
   
    if tip == 'AL':
       tip = 'SAT'
    else:
       tip = 'AL'
    try:
       print(client.futures_create_order(
       symbol=ticker,
       type='MARKET',
       side=tip,
       quantity=miktar,
       reduceOnly=True))
       print(tip+" başarıyla kapatıldı")
    #ReduceOnly ile bu sadece mevcut emri kapatır ve yeni bir emir açmaz.
    except:
       print("Kapatılacak " + tip + " emri yok")
   

def açıkEmir(tip:str):
    
    global ticker
    global kaldıraç
    global miktar
    emirAl = client.futures_change_leverage(symbol=ticker, leverage=kaldıraç)
    print(client.futures_create_order(
       symbol=ticker,
       type='MARKET',
       side=tip,
       quantity=miktar))
    print(tip+" başarıyla yerleştirildi")



def canlıFiyat():
    
    global canlı_fiyat
    global saat_hızı
    global emir_noktası
    global ara_emir_noktası
    
    while True:
       data = (client.futures_symbol_ticker(symbol=ticker))
       canlı_fiyat = float(data['price'])
       print(f'Güncel Fiyat {canlı_fiyat}, Emir Noktası {emir_noktası}, ara emir noktası {ara_emir_noktası}')
       time.sleep(saat_hızı)
global canli_fiyat
global zamanlama_hizi
global siparis_noktasi
global ara_siparis_noktasi

while True:
   data = (client.futures_symbol_ticker(symbol=ticker))
   canli_fiyat = float(data['price'])
   print(f'Şu anki fiyat {canli_fiyat} ve sipariş noktası {siparis_noktasi} ve ara sipariş noktası {ara_siparis_noktasi}')
   time.sleep(zamanlama_hizi)
def bölge_belirleyici_islem():
    global bölgeler
    global canli_fiyat
    global bölge_icinde
    while True:
        c = len(bölgeler)
        sayac = 0
        bulundu  = False
         while sayac != c:
            bölge = bölgeler[sayac]
            if canli_fiyat <= bölge[0] and canli_fiyat >= bölge[1]:
                bulundu = True
            sayac = sayac + 1
        
        if bulundu:
            bölge_icinde = True
        else:
        bölge_icinde = False
def order_execution():
    global order_point
global live_price
global intermediate_order_point

global clock_speed

global position_long_open
global position_short_open

global long_order_point_shifted
global short_order_point_shifted

global trailing_long_base
global trailing_short_base

global initial



while True:

    
    if live_price > order_point:
        
        if position_long_open != True:
            
            
            if position_short_open:

                if short_order_point_shifted:
                    reset()
                    short_order_point_shifted = False
                    print(f'Kar Alındı ve Pozisyonlar {trailing_long_base} oranında karla kapatıldı.')
                    
                
                CloseOrder('SELL')
                position_short_open = False

            

            openOrder('BUY')
            order_point = live_price
            intermediate_order_point  = order_point
            position_long_open  = True

    elif live_price < order_point:
        
        
        if position_short_open != True:
            
            if position_long_open:

                if long_order_point_shifted:
                    reset()
                    long_order_point_shifted = False
                    print(f'Kar Alındı ve Pozisyonlar {trailing_short_base} oranında karla kapatıldı.')
                    
                
                CloseOrder('BUY')
                position_long_open = False

            
                
            openOrder('SELL')
            order_point = live_price
            intermediate_order_point  = order_point
            position_short_open = True

    else:
        print("Fiyat başlangıç değerinde.")
    
def reset():
global order_point
global intermediate_order_point
global trailing_long_target
global trailing_long_base

global trailing_short_target
global trailing_short_base

intermediate_order_point = order_point

trailing_long_target = 5
trailing_long_base = 3

trailing_short_target = 5
trailing_short_base = 3
print("Değerler sıfırlandı.")

if name == 'main':
getLivePrice_thread = threading.Thread(target=getLivePrice)
getLivePrice_thread.start()
zone_identifier_process_thread = threading.Thread(target=zone_identifier_process)
zone_identifier_process_thread.start()

order_execution_thread = threading.Thread(target=order_execution)
order_execution_thread.start()
print('Bot Başlatılıyor')
FiyatGüncelleyici = threading.Thread(target=getLivePrice)
FiyatGüncelleyici.start()
time.sleep(2)
BölgeBelirleyici_Thread = threading.Thread(target=zone_identifier_process)
BölgeBelirleyici_Thread.start()
EmirYürütücü_Thread = threading.Thread(target=order_execution)
EmirYürütücü_Thread.start()
time.sleep(.2)
KârHedefiKaydırıcı_Thread = threading.Thread(target=target_chaser)
KârHedefiKaydırıcı_Thread.start()
KârYürütücü_Thread = threading.Thread(target=profit_taker)
KârYürütücü_Thread.start()
