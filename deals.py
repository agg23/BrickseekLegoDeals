import sys

import brickseek
import brickfront
import time

from mail import *

if len(sys.argv) != 4:
	print("Usage:\n\t./deals.py [from email] [from email password] [to email]")
	exit(1)

bricksetApiKey = ""
useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"

fromAddress = sys.argv[1]
fromAddressPassword = sys.argv[2]
toAddress = sys.argv[3]

brickseekApi = brickseek.Brickseek()
brickfrontClient = brickfront.Client(bricksetApiKey)

walmartSkusToSetNumber = {
    47335830: 10702,
    41004055: 10696,
    355348849: 70618,
    399600388: 70617,
    54595518: 70909,
    55126150: 60141,
    47335764: 60110,
    51720888: 75155,
    184758738: 70908,
    51471177: 75149,
    51720865: 31052,
    47335714: 21125,
    40996357: 10698,
    55126212: 75172,
    55126184: 70907,
    47335762: 70603,
    51471174: 75147,
    187472787: 76081,
    51720851: 60102,
    55126168: 70351,
    51720884: 70593,
    51471176: 75148,
    51720889: 75153,
    51720866: 31053,
    51720879: 70589,
    51720862: 60134,
    51720897: 76059,
    55126185: 70904,
    51720878: 70588,
    55126183: 70903,
    55126219: 76077,
    185857976: 76080,
    51720890: 75152,
    55126162: 60152,
    47335806: 76047,
    55126218: 75169,
    55126166: 70350,
    47335769: 75117,
    55126151: 60137,
    101948702: 75173,
    51720855: 60121,
    47335734: 31048,
    47335759: 75137,
    32703654: 60048,
    149099288: 76079,
    40996313: 10693,
    55126161: 60150,
    55126158: 60147,
    55126142: 31059,
    55126134: 31060,
    47335724: 21123,
    45059348: 21119,
    47335814: 76053,
    55126182: 70902,
    51720881: 70591,
    41004852: 10692,
    55126141: 31058,
    47348007: 60117,
    55126160: 60148,
    47335738: 75131,
    55126140: 31057,
    51720850: 60120,
    55126139: 31056,
    51720848: 60100,
    55126155: 60144,
    55126157: 60146,
    480319843: 75189,
    55126254: 70917,
    606959421: 60161,
    163329791: 75187,
    754096201: 75179,
    334504577: 70615,
    665818996: 31069,
    928479925: 60160,
    482121496: 70614,
    322045533: 70612,
    618377518: 60154,
    121719463: 60153,
    319232959: 41187,
    755063597: 75184,
    239444704: 60159,
    55126266: 76083,
    55126154: 60138,
    744249417: 31066,
    797736314: 31068,
    963121977: 31067,
    937661939: 70611,
    877034674: 70608,
    314281811: 70609,
    55126259: 75183,
    55126220: 75168,
    51720855: 60121,
    180593349: 76087,
    946006306: 75188,
    432807058: 41188,
    55126201: 21134,
    490776812: 21135,
    519970525: 60166,
    55126181: 70626,
    961978591: 76088,
    55126199: 21133,
    821527659: 75177,
    55126152: 60139,
    55126138: 31065,
    248181038: 60165,
    512020654: 75530,
    55126221: 75170,
    55126148: 60135,
    951814057: 75190,
    871447697: 60167,
    405515204: 21136,
    55126153: 60140,
    123040621: 76084,
    55126211: 75171,
    681187061: 70354,
    601405208: 60155,
    748224511: 75176,
    55126205: 10708,
    507356910: 41239,
    55126261: 75186,
    55126251: 70916,
    55126257: 75180,
    55126260: 75185,
    55126263: 75532,
    55126255: 75178,
    55126252: 70915,
    55126208: 21132,
    55126249: 70914,
    341280213: 70353,
    45064378: 75105,
    31196207: 60046,
    45059380 :75102,
    239480739: 70355,
    55126179: 70625,
    705596439: 76086,
    55126143: 31064,
    55126276: 70610,
    55126258: 75182,
    148532933: 60151,
    55126176: 70623,
    55126178: 70624,
    55126136: 31063,
    55126262: 75531,
    328835713: 70607,
    914016362: 75526,
    54595517: 70901,
    167077277: 76076,
    55126133: 31062,
    55126177: 70622,
    123199450: 60142,
    55126164: 70348,
    55126165: 70349,
    55126256: 75167,
    55126253: 75166,
    930878869: 70361,
    55126159: 60149,
    55126123: 10737,
    55126217: 75165,
    47335809: 76044,
    285650271: 70606,
    55126213: 75161,
    443431987: 60157,
    55126203: 75160,
    917517401: 60163,
    55126173: 70621,
    55126149: 60136,
    55126156: 60145,
    55126204: 75162,
    55126210: 75163,
    55126163: 70347,
    47347999: 75129,
    55126202: 10706,
    55126196: 10707,
    55126206: 10709
}

walmartAddresses = [
    "2399 S State Road 46 Terre Haute IN 47803",
    "5555 S Us Hwy #41 Terre Haute IN 47802"
]

zipCode = "47803"

walmartItems = [brickseekApi.createWalmartItem(sku) for sku in walmartSkusToSetNumber]
walmartItemsCount = len(walmartItems)

import traceback

bricksetItems = {}

brickseekApi.updateUserAgent(useragent)

i = 0
while i < len(walmartItems):
    item = walmartItems[i]
    print("Updating item %d out of %d" % (i + 1, walmartItemsCount))
    try:
        errorCode = item.fetchLocalInventory(zipCode)
        
        if errorCode == 403:
            print("Please enter updated cf_clearance cookie:")
            cf_clearance = input()
            print("Please enter updated cfduid cookie:")
            cfduid = input()
            
            brickseekApi.updateCookies(cf_clearance, cfduid)
            continue

        setNumber = str(walmartSkusToSetNumber[item.sku])

        setList = brickfrontClient.getSets(query=setNumber)
        for setItem in setList:
            if setItem.number == setNumber:
                bricksetItems[item] = {"url": setItem.bricksetURL, "imageUrl": setItem.imageURL, 
                                       "msrp": setItem.priceUS, "set": setNumber,
                                       "pieces": setItem.pieces}
                break
    except:
        traceback.print_exc()
        print("Failed to update item %d with sku %d" % (i + 1, item.sku))
        time.sleep(8)
            
    time.sleep(2)
    i += 1
    
print("Updated %d items" % (walmartItemsCount))

walmartStores = [brickseekApi.lookupStore(address) for address in walmartAddresses]

email = generateEmailString(fromAddress, toAddress, walmartItems, walmartStores, bricksetItems)

sendEmail(fromAddress, fromAddressPassword, toAddress, email)
