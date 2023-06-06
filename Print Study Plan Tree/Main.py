from turtle import color, width
import requests
from bs4 import BeautifulSoup
from pyvis.network import Network
HashedMaterials = {}
Graph = {}
Start = []
NeedPreq = {}
ParentPreq = {}
def BFS(Curr):
    global HashedMaterials
    global Graph
    global NeedPreq
    global Start
    if Curr not in Graph:
        return
    for Course in Graph[Curr]:
        NeedPreq[Course] -= 1
        if NeedPreq[Course] == 0:
            # Net.add_edge(Curr, HashedCourse["course_id"])
            Start.append(Course)
def LetsSort(X):
    global ParentPreq
    Ans = 0
    if X in ParentPreq:
        Ans = -ParentPreq[X]
    return (Ans, X)


def CleanData(Data):
    for i in range(len(Data)):
        Data[i] = Data[i].strip()

def getTree(URL):
    global HashedMaterials
    global Graph
    global NeedPreq
    global Start
    global ParentPreq
    Net = Network(directed=True, width="100%", height="100%")
    Net.toggle_physics(False)
    Page = requests.get(URL).text
    Soup = BeautifulSoup(Page, "lxml")

    


    Content = Soup.find("section", {"class": "mission-area ptb-100"})
    FirstItem = Content.find_all("li", {"class": "program-box"})
    PageName = Soup.find("div", {"class": "section-title"}).text


    
    
    
    for Item in FirstItem:
        Table = Item.table
        MaterialType = " ".join(Item.find(
            "div", {"class": "program-title"}).text.split(" ")[:3])
        Trs = Table.find_all("tr")[1:-1]
        

        Color = "blue"
        if MaterialType == "متطلب جامعة اجباري":
            Color = "#B22222"
        elif MaterialType == "متطلب جامعة حرة":
            Color = "#80c9f8"
        elif MaterialType == "متطلب كلية حرة":
            Color = "#c40a3d"
        elif MaterialType == "متطلب كلية اجباري":
            Color = "#39d6ab"
        elif MaterialType == "متطلب تخصص اجباري":
            Color = "#39d6ab"
        elif MaterialType == "متطلب تخصص حرة":
            Color = "#671f92"
        elif MaterialType == "متطلبات استدراكي اجباري":
            Color = "#9d9b92"
        for Tr in Trs:
            DataCourse = Tr.text.strip().split("\n")
            
            CleanData(DataCourse)
            DataCourse = list(filter(lambda x: x != '', DataCourse))
            if(len(DataCourse) < 5):
                DataCourse.append('')
            
            
            HashedMaterials[DataCourse[1]] = {
                "course_id": DataCourse[1],
                "course_name": DataCourse[2],
                "need": [],
                "MaterialType": MaterialType,
                "Color": Color
            }
            if len(DataCourse[-1]):
                ManyPreq = DataCourse[-1].split(",")
                for Course in ManyPreq:
                    Course = Course.strip()
                    HashedMaterials[DataCourse[1]]["need"].append(Course)
                    if Course not in Graph:
                        Graph[Course] = []
                        ParentPreq[Course] = 0
                    Graph[Course].append(DataCourse[1])
                    ParentPreq[Course] += 1

                    if DataCourse[1] not in NeedPreq:
                        NeedPreq[DataCourse[1]] = 0
                    NeedPreq[DataCourse[1]] += 1


    for Key, Val in HashedMaterials.items():
        if len(Val["need"]) == 0:
            Start.append(Val["course_id"])


    

    Start.sort(key=LetsSort)
    Start.append("-0000")
    CurrX = 0
    CurrY = 0
    while len(Start) > 0:
        Curr = Start[0]

        Start.pop(0)
        if Curr == "-0000":
            # print("#"*20)
            if len(Start):
                CurrY += 200
                CurrX = 0
                # Start.sort(key=LetsSort)
                Start.append("-0000")
            continue

        
        HashedCourse = HashedMaterials[Curr]
        Net.add_node(HashedCourse["course_id"],
                    HashedCourse["course_name"] + "\n(" + HashedCourse["MaterialType"] + ")", x=CurrX, y=CurrY, color=HashedCourse["Color"])
        if len(HashedCourse["need"]) != 0:
            for Course in HashedCourse["need"]:
                Net.add_edge(Course, HashedCourse["course_id"])
        CurrX += 200
        BFS(Curr)
    
    Net.show("index.html")

print("Enter URL : ")
URL = input()
getTree(URL)