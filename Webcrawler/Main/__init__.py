from lxml import html
import requests

print("Begin\n")

page = requests.get('http://www.ourkids.net/ontario-private-schools.php')
tree = html.fromstring(page.content)
links = tree.xpath("//body//table//a[starts-with(@href, '/school/') and not(contains(@href, 'adv-search-results'))]/@href")

base = "http://www.ourkids.net"
results = {}
for ref in links:
    
    link=base+ref
    #print(link)
    schoolPage = requests.get(link)
    schoolTree = html.fromstring(schoolPage.content)
    schoolName = schoolTree.xpath("//body//h1/text()")[0]
    
    print("Extracting data from "+schoolName)
    
    generalInfo = schoolTree.xpath("//body//div/comment()[.='MOBILE CTA HEADER']/..//div[@class='large-3 medium-3 small-5 columns']/strong[not(contains(text(), 'E-Brochure:'))]/text()")
    generalInfo2 = schoolTree.xpath("//body//div/comment()[.='MOBILE CTA HEADER']/..//div[@class='large-9 medium-9 small-7 columns']/text()")
    
    generalInfo3 = []
    subList = []
    
    #print(generalInfo)
    #print(generalInfo2)
    
    if(len(generalInfo) != len(generalInfo2)):
        generalInfo3 = schoolTree.xpath("//body//div/comment()[.='MOBILE CTA HEADER']/..//div[@class='large-3 medium-3 small-5 columns']/strong/text()|//body//div/comment()[.='MOBILE CTA HEADER']/..//div[@class='large-9 medium-9 small-7 columns']/text()")
        #print(generalInfo3)
        
        i = 0
        j = 0
        while (i < len(generalInfo3) and j < len(generalInfo)):
            #print(generalInfo3[i+1].strip(), generalInfo[j+1].strip())
            if (generalInfo3[i+1].strip() == generalInfo[j+1].strip()):
                subList.append((generalInfo3[i].strip(), ""))
                #print((generalInfo3[i].strip(), ""))
                i+=1
            else:
                subList.append((generalInfo3[i].strip(), generalInfo3[i+1].strip()))
                #print((generalInfo3[i].strip(), generalInfo3[i+1].strip()))
                i+=2
                j+=1
    
    
    
    else:
        for i in range (len(generalInfo)):
            if ("Brochure" in generalInfo[i].strip()):
                continue
            subList.append((generalInfo[i].strip(), generalInfo2[i].strip()))
    
    #print(schoolName)
    enrollmentInfo = schoolTree.xpath("(//body//div[@id='panelStudent']//table)[1]//td//text()")
    #print(enrollmentInfo)
    subList2 = []
    for i in range(len(enrollmentInfo)/2):
        subList2.append((enrollmentInfo[i*2].strip(), enrollmentInfo[i*2+1].strip()))
    #print(subList2)     
    results[schoolName]=(subList,subList2)   
    
#print(results)

print("\nPrinting final results\n")

for key, value in results.items():
    print(key+"\n\nGeneral Info")
    for pair in value[0]:
        print(pair[0]+" "+pair[1])
    print("\nEnrollement Info")   
    for pair in value[1]:
        print(pair[0]+": "+pair[1])
    print("\n")
print("End")