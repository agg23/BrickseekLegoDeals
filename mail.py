from PIL import Image
import requests
from io import BytesIO

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import smtplib

def generateImageAttachments(ebayItems):
    images = {}
    
    for (i, item) in enumerate(ebayItems):
        response = requests.get(item.imageUrl)
        img = Image.open(BytesIO(response.content))
        
        mimeImage = MIMEImage(img)
        mimeImage.add_header("Content-ID", "<image" + i + ">")
        
        images[item] = {"image": mimeImage, "cid": "image" + i}
        
    return images

def generateBody(innerHTML):
    return "<html><body>" + innerHTML + "</body></html>"

def generateEbayTable(ebayItems):
    innerHTML = ""
    for i in range(0, min(len(ebayItems), 10)):
        item = ebayItems[i]
        innerHTML += "<tr><td><img style=\"max-width: 200px; max-height: 200px;\" src=\"{}\"/></td><td>{}</td><td>${:.2f}</td></tr>".format(item.imageUrl, item.name, item.price)
    
    return "<table><tr><th></th><th>Name</th><th>Cost</th></tr>" + innerHTML + "</table>"

def generateBestDeal(items, stores, bricksetItems):
    bestDealDiscount = 0.0
    bestItem = None
    bestInventory = None
    bestBricksetItem = None
    
    for item in items:
        maxDiscount = 0
        maxDiscountInventory = None
        
        bricksetItem = bricksetItems.get(item, None)
        imageUrl = ""
        url = ""
        msrp = 0
        setNumber = 0
        
        if not bricksetItem:
            continue
                
        msrp = float(bricksetItem["msrp"])
        
        if not isinstance(item.inventory, list):
            continue
        
        for inventory in item.inventory:
            if inventory.store not in stores:
                continue
                
            discount = 100*(1 - inventory.price/msrp)
            
            if discount > maxDiscount:
                maxDiscount = discount
                maxDiscountInventory = inventory
                
        if maxDiscount > bestDealDiscount:
            bestDealDiscount = maxDiscount
            bestItem = item
            bestInventory = maxDiscountInventory
            bestBricksetItem = bricksetItem
                
    if bestInventory:
        url = bestBricksetItem["url"]
        imageUrl = bestBricksetItem["imageUrl"]
        msrp = float(bestBricksetItem["msrp"])
        setNumber = int(bestBricksetItem["set"])
        discount = 100*(1 - bestInventory.price/msrp)
        pieces = int(bestBricksetItem["pieces"])
        
        if pieces == 0:
            pieces = 1
                
        return ("<div style=\"display: inline-block; text-align: center; font-size: 22;\" class=\"best\">"
                    "<img style=\"max-width: 400px; max-height: 400px;\" src=\"{}\"/>"
                    "<a href=\"{}\"><div style=\"font-size: 18;\" class=\"number\">{}</div></a>"
                    "<div style=\"font-size: 26;\" class=\"name\">{}</div>"
                    "<a href=\"{}\"><div class=\"price\">${:0.2f}</div></a>"
                    "<div class=\"ppp\">PPP: ${:0.4f}</div>"
                    "<div class=\"discount\">Discount: {:0.0f}%</div>"
                    "<div style=\"font-size: 12;\" class=\"store\">{}</div></div>").format(imageUrl, url, setNumber, bestItem.name, bestItem.getURL(), bestInventory.price, bestInventory.price/pieces, discount, bestInventory.store.address)
    
    return ""

def generateSortedLego(items, stores, bricksetItems):
    sortedItems = []
    
    for item in items:
        bricksetItem = bricksetItems.get(item, None)
        maxDiscount = 0
        
        msrp = 0
            
        if bricksetItem:
            msrp = float(bricksetItem["msrp"])
            
        if not isinstance(item.inventory, list):
            continue
                
        for inventory in item.inventory:
            if inventory.store not in stores:
                continue
                
            
            try:  
                discount = 100*(1 - inventory.price/msrp)
                
                if discount > maxDiscount:
                    maxDiscount = discount
            except:
                pass
            
        sortedItems.append({"discount": maxDiscount, "item": item})
    
    sortedItems.sort(key=lambda item: item["discount"], reverse=True)
    return list(map(lambda item: item["item"], sortedItems))

def generateBrickseekLegoTable(items, stores, bricksetItems):
    innerHTML = ""
    for item in items:
        if not isinstance(item.inventory, list):
            continue
        
        for inventory in item.inventory:
            if inventory.store not in stores:
                continue
                            
            bricksetItem = bricksetItems.get(item, None)
            imageUrl = ""
            url = ""
            msrp = 1
            setNumber = 0
            pieces = 1
            
            if bricksetItem:
                url = bricksetItem["url"]
                imageUrl = bricksetItem["imageUrl"]
                msrp = float(bricksetItem["msrp"])
                setNumber = int(bricksetItem["set"])
                if bricksetItem["pieces"]:
                    pieces = int(bricksetItem["pieces"])
                    
                    if pieces == 0:
                        pieces = 1
            
            innerHTML += "<tr><td><img style=\"max-width: 200px; max-height: 200px;\" src=\"{}\"/></td><td><a href=\"{}\">{}</a></td><td>{}</td><td>{}</td><td>{}</td><td><a href=\"{}\">${:.2f}</a></td><td>${:.2f}</td><td>{:.0f}%</td><td>{}</td><td>${:.4f}</td></tr>".format(imageUrl, url, setNumber, item.name, inventory.store.address, inventory.forSale, item.getURL(), inventory.price, msrp, 100*(1 - inventory.price/msrp), pieces, inventory.price/pieces)
    
    return "<table><tr><th></th><th>Set</th><th>Name</th><th>Store</th><th>Available</th><th>Cost</th><th>MSRP</th><th>Discount</th><th>Pieces</th><th>PPP</th></tr>" + innerHTML + "</table>"

def generateEmailString(fromAddress, toAddress, walmartItems, walmartStores, bricksetItems):
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Daily Deals'
    msgRoot['From'] = fromAddress
    msgRoot['To'] = toAddress
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    # We reference the image in the IMG SRC attribute by the ID we give it below

    sortedLego = generateSortedLego(walmartItems, walmartStores, bricksetItems)

    html = generateBestDeal(walmartItems, walmartStores, bricksetItems)
    html += generateBrickseekLegoTable(sortedLego, walmartStores, bricksetItems)

    msgText = MIMEText(generateBody(html), 'html')
    msgRoot.attach(msgText)

    return msgRoot.as_string()

def sendEmail(fromAddress, fromAddressPassword, toAddress, message):
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(fromAddress, fromAddressPassword)
    smtp_server.sendmail(fromAddress, toAddress, message)
    smtp_server.quit()
