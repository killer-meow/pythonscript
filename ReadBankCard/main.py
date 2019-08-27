# coding=utf8
from smartcard.System import readers
from smartcard.util import toHexString
import json
import os
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
########################################
###NIAN HUA #############@)!()&!!#######
cardid = ''
startdata = '2001.01.01'
enddata = '2029.12.31'
dataok = False
cardtype = ''
cardname = ''
username = ''
useridcardtype = ''
userid = ''
paylog = []
show_flag = False

allcarddata = {'cardid':'','startdata':'','enddata':'','cardtype':'','cardname':'','username':'','useridcardtype':'','userid':'','paylog':[]}


def var_init():

	global cardid,startdata,enddata,dataok,cardtype,cardname,username,useridcardtype,userid,paylog,show_flag,allcarddata

	cardid = ''
	startdata = '2001.01.01'
	enddata = '2029.12.31'
	dataok = False
	cardtype = ''
	cardname = ''
	username = ''
	useridcardtype = ''
	userid = ''
	paylog = []
	allcarddata = {'cardid':'','startdata':'','enddata':'','cardtype':'','cardname':'','username':'','useridcardtype':'','userid':'','paylog':[]}


def show_something(sign,title,data):

    if sign == True:

        print title

        print '-' * 30

        print data

        print '-' * 30

def get_records_consumption(connection):

    global paylog

    for i in range(10):

    	try:

            onepaylog = {'paytime':'','paynumber':'','paylocation':'','paytype':''}

            PAYLOGAT = [0x00,0xb2,i+1,0x5c,0x00]


            card,sw1,sw2 = connection.transmit(PAYLOGAT)

            show_something(show_flag,'SEND INFORMATION',str(PAYLOGAT))

            card = toHexString(card)

            show_something(show_flag,'WAIT INFORMATION NOW',card)

            card = card.split(' ')

            paytime = '20' + card[0] + u'年' + card[1] + u'月' + card[2] + u'日 ' + card[3] + u':' + card[3] + u':' + card[4]

            onepaylog['paytime'] = paytime.encode('utf-8')


            paynumber = int(card[6])*100000000 + int(card[7])*1000000 + int(card[8])*10000 + int(card[9])*100 + int(card[10])*1 + int(card[11])*0.01

            onepaylog['paynumber'] = '{:.2f}'.format(paynumber)

            if card[-3] == '01':

                paytype = u'提款/现金付款'

            elif card[-3] == '30':

                paytype = u'查询可用现金'

            else:

                paytype = u'POS机交易'

            onepaylog['paytype'] = paytype.encode('utf-8')

            paylocation = ''

            for i in range(20):

                paylocation += chr(int(card[22 + i],16))

            onepaylog['paylocation'] = paylocation.decode('gbk').encode('utf-8')
            
            paylog.append(onepaylog)

        except:

            pass



def get_user_information(connection):

    global username
    global useridcardtype
    global userid
    USERIDAT = [0x00,0xb2,0x01,0x0c,0x00]
    card,sw1,sw2 = connection.transmit(USERIDAT)
    show_something(show_flag,'SEND INFORMATION',str(USERIDAT))
    card = toHexString(card)
    show_something(show_flag,'WAIT INFORMATION NOW',card)
    card = card.split(' ')
    for i in range(len(card)-1):
        if card[i] == '9F' and card[i+1] == '61':
            for j in range(18):
                userid += card[i+3+j][1]
            break
    for i in range(len(card)-1):
        if card[i] == '9F' and card[i+1] == '62':
            if card[i+3] == '00':
                useridcardtype = u'身份证'.encode('utf-8')
            else:
                useridcardtype = u'其他证件'.encode('utf-8')
    for i in range(len(card)-1):
        if card[i] == '5F' and card[i+1] == '20':
            for j in range(int(card[i+2],16)):
                username += chr(int(card[i+3+j],16))
            break


def get_card_data(connection):

    global startdata
    global enddata
    global dataok
    DATAAT = [0x00,0xb2,0x01,0x14,0x00]
    DATAAT2  = [0x00,0xb2,0x01,0x0c,0x00]

    card,sw1,sw2 = connection.transmit(DATAAT)
    show_something(show_flag,'SEND INFORMATION',str(DATAAT))
    card = toHexString(card)
    show_something(show_flag,'WAIT INFORMATION NOW',card)
    card = card.split(' ')

    for i in range(len(card)-1):
        if card[i] == '5F' and card[i+1] == '25':
            startdata = '20' + card[i+3] + '.' + card[i+4] + '.' +card[i+5]
            dataok = True
            break

    for i in range(len(card)-1):
        if card[i] == '5F' and card[i+1] == '24':
            enddata = '20' + card[i+3] + '.' + card[i+4] + '.' +card[i+5]
            dataok = True
            break

    if dataok == False:
        card,sw1,sw2 = connection.transmit(DATAAT2)
        show_something(show_flag,'SEND INFORMATION',str(DATAAT2))
        card = toHexString(card)
        show_something(show_flag,'WAIT INFORMATION NOW',card)
        card = card.split(' ')
        for i in range(len(card)-1):
            if card[i] == '57':
                enddata = '20' + card[i+12] + '.' + card[i+13] + '.' + '30'
                dataok = True
                break


def get_card_id(connection):
    'Get user card id ,But that could go wrong'

    global cardid
    CARDID1  = [0x00,0xb2,0x01,0x14,0x00]
    CARDID2  = [0x00,0xb2,0x01,0x0c,0x00]

    card,sw1,sw2 = connection.transmit(CARDID1)
    show_something(show_flag,'SEND INFORMATION',str(CARDID1))
    card = toHexString(card)
    show_something(show_flag,'WAIT INFORMATION NOW',card)
    card = card.split(' ')

    for i in range(len(card)-1):
        if card[i] == '5A':
            for j in range(int(card[i+1],16)):
                cardid += card[i+2+j]
            cardid = cardid.replace('F','')
            break

    if len(cardid) < 8:
        card,sw1,sw2 = connection.transmit(CARDID2)
        show_something(show_flag,'SEND INFORMATION',str(CARDID2))
        card = toHexString(card)

        print card
        show_something(show_flag,'WAIT INFORMATION NOW',card)
        card = card.split(' ')

        for i in range(len(card)-1):
            if card[i] == '57':
                for j in range(10):
                    cardid += card[i+2+j]
                cardid = cardid.replace('D','')
                break

def card_select(connection):

    SELECT  = [0x00,0xa4,0x04,0x00,0x07,0xa0,0x00,0x00,0x03,0x33,0x01,0x01]

    data,sw1,sw2 = connection.transmit(SELECT)

    show_something(show_flag,'SEND INFORMATION',str(SELECT))

    data = toHexString(data)

    show_something(show_flag,'WAIT INFORMATION NOW',data)


def card_init():
    
    r = readers()  # get sdr id card number

    print 'SELECT' + str(r[0]) + 'IDCARD SYSTEMS'

    connection  = r[0].createConnection()

    connection.connect()

    return connection

########################################

def change():

	var_init()
######################################################3

    try:
        connection = card_init()
        card_select(connection)
        get_card_id(connection)

        if userid=="000000000000000000":
            userid="******************"
        print userid
        allcarddata['cardid'] = cardid
        get_card_data(connection)
        allcarddata['startdata'] = startdata
        allcarddata['enddata'] = enddata
        get_user_information(connection)
        allcarddata['userid'] = userid
        allcarddata['useridcardtype'] = useridcardtype
        allcarddata['username'] = username
        get_records_consumption(connection)
        allcarddata['paylog'] = paylog

#######################################################
        print username
        return json.dumps(allcarddata)

    except:

        data = {'cardid':'&nbsp;','startdata':'','enddata':'','cardtype':' ','cardname':' ','username':' ','useridcardtype':' ','userid':' ','paylog':[]}

        return json.dumps(data)

if __name__ == '__main__':
    
    print change()



