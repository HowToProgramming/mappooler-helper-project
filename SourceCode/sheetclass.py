from start import osu, atr, base64
from os import path

class sheet():
    def __init__(self, sheeturl, index, mappooler, mappooleramt, max_score_rating):
        self.tour_id = sheeturl.split("/")[-2]
        self.worksheet = atr.open_by_url(sheeturl).get_worksheet(index)
        self.mappooler = mappooler
        self.mappooleramt = mappooleramt
        self.cellval = self.worksheet.range("A1:R100")
        self.val = []
        self.rc = -1
        for i in self.cellval:
            if self.rc != i.row - 1:
                self.val.append([])
                self.rc += 1
            self.val[self.rc].append(i.value)
        self.max_score_rating = max_score_rating

    def update_sheet(self):
        self.cellval = self.worksheet.range("A1:R100")
        newval = []
        self.rc = -1
        for i in self.cellval:
            if self.rc != i.row - 1:
                newval.append([])
                self.rc += 1
            newval[self.rc].append(i.value)
        self.val = newval

    def findrow(self, colstart, colfinish):
        self.update_sheet()
        r = 1
        while self.val[r][colstart:colfinish + 1] != [""] * (colfinish - colstart + 1):
            r += 1
        return r

    def add_map(self, beatmapid, t, comments):
        self.update_sheet()
        row = self.findrow(0, 4) + 1
        self.worksheet.update_cell(row, 1, self.mappooler)
        self.worksheet.update_cell(row, 2, "https://osu.ppy.sh/b/{}".format(beatmapid))
        if self.val[0][2] != "":
            beatmap = osu.beatmaps(beatmapid)
            self.worksheet.update_cell(row, 3, "{} - {} [{}]".format(beatmap['artist'], beatmap['title'], beatmap['version']))
        self.worksheet.update_cell(row, 4, t)
        self.worksheet.update_cell(row, 5, comments)
    
    def vote(self, beatmapid, statement):
        self.update_sheet()
        row = 0; col = 0
        for i in self.val:
            row += 1
            if i[1].split("/")[-1] == str(beatmapid):
                break
        for bruh in self.val[0]:
            col += 1
            if bruh == self.mappooler:
                break
        self.worksheet.update_cell(row, col, str(statement))
    
    def pick(self, beatmapid):
        self.update_sheet()
        mappicker = ""; t = ""
        for i in self.val:
            if i[1].split("/")[-1] == str(beatmapid):
                mappicker += i[0]
                t = i[3]
                break
        types = []
        for i in range(1, len(self.val)):
            if self.val[i][5 + self.mappooleramt] == "":
                break
            types.append(self.val[i][5 + self.mappooleramt])
        
        beatmap = osu.beatmaps(str(beatmapid))
        row = 1
        for tt in types:
            row += 1
            if tt == t:
                break
        self.worksheet.update_cell(row, 7 + self.mappooleramt, "=HYPERLINK(\"https://osu.ppy.sh/b/{}\", \"{} - {}\")".format(beatmapid, beatmap['artist'], beatmap['title']))
        self.worksheet.update_cell(row, 8 + self.mappooleramt, beatmap['version'])
        self.worksheet.update_cell(row, 9 + self.mappooleramt, beatmap['creator'])
        self.worksheet.update_cell(row, 10 + self.mappooleramt, "{:02f}".format(float(beatmap['difficultyrating'])))
        self.worksheet.update_cell(row, 11 + self.mappooleramt, "{}:{:02d}".format(int(beatmap['hit_length']) // 60, int(beatmap['hit_length']) % 60))
        self.worksheet.update_cell(row, 12 + self.mappooleramt, "{} / {}".format(beatmap['diff_overall'], beatmap['diff_drain']))
        self.worksheet.update_cell(row, 13 + self.mappooleramt, mappicker)

    def checkAgreement(self):
        self.update_sheet()
        agreement = []
        # 5 6 7 8 df2+1
        for i in range(len(self.val)):
            sumagreement = 0
            for j in range(5,5 + self.mappooleramt):
                if i == 0:
                    continue
                try:
                    if float(self.val[i][j]) > self.max_score_rating:
                        sumagreement += self.max_score_rating
                    else:
                        sumagreement += float(self.val[i][j])
                except:
                    continue
            if(sumagreement >= self.mappooleramt * self.max_score_rating / 2):
                agreement.append(int(self.val[i][1].split("/")[-1]))
        return agreement

    def pickAgreement(self):
        self.update_sheet()
        for i in self.checkAgreement():
            self.pick(i)
    
    def showAllMaps(self):
        self.update_sheet()
        t = self.get_database()
        t = [i['maps'] for i in t if i['tour_id'].replace("\n", "") == self.tour_id]
        try:
            t = t[0]
        except:
            pass
        artist_title_version = ["{} - {} [{}]".format(i.split("|")[0], i.split("|")[1], i.split("|")[2]) for i in t]
        mapindatabase = [i.split("|")[-1] for i in t]
        beatmapsid = []
        type_ = []
        for i in self.val:
            if i == self.val[0]:
                continue
            beatmapsid.append(i[1].split("/")[-1])
            type_.append(i[3])
        str_beatmap_data = ""
        for i in range(1, len(beatmapsid) - 1):
            sumagreement = 0
            for j in range(5,5 + self.mappooleramt):
                try:
                    if float(self.val[i][j]) > self.max_score_rating:
                        sumagreement += self.max_score_rating
                    else:
                        sumagreement += float(self.val[i][j])
                except:
                    continue
            try:
                if beatmapsid[i - 1] in mapindatabase:
                    str_beatmap_data += "[{}] {} - https://osu.ppy.sh/b/{} ({}/{} Agreements)\n".format(type_[i - 1], artist_title_version[mapindatabase.index(beatmapsid[i - 1])], beatmapsid[i - 1], sumagreement, self.mappooleramt * self.max_score_rating)
                else:
                    bmdata = osu.beatmaps(beatmapsid[i - 1])
                    str_beatmap_data += "[{}] {} - {} [{}] - https://osu.ppy.sh/b/{} ({}/{} Agreements)\n".format(type_[i - 1], bmdata['artist'], bmdata['title'], bmdata['version'], beatmapsid[i - 1], sumagreement, self.mappooleramt * self.max_score_rating)
                    self.write_database([beatmapsid[i - 1]])
            except:
                pass
        return str_beatmap_data
    
    @staticmethod
    def _get_str_map_id_(mapid):
        bmdata = osu.beatmaps(mapid)
        return "{}|{}|{}|{}".format(bmdata['artist'], bmdata['title'], bmdata['version'], mapid)

    @staticmethod
    def get_database():
        tourneys = []
        if not path.isfile('db.mph'):
            return tourneys
        with open('db.mph', 'r') as database:
            database = database.readlines()
            for i in range(0, len(database), 2):
                try:
                    tourneys.append({'tour_id': database[i].replace("\n", ""), 'maps': database[i+1].replace("\n", "").split("&&&")})
                except:
                    tourneys.append({'tour_id': database[i], 'maps': []})
        return tourneys
    
    def write_database(self, mapid):
        if not path.isfile("db.mph"):
            with open('db.mph', 'w+') as database:
                database.write(self.tour_id)
                database.write("\n")
                strid = "&&&".join([self._get_str_map_id_(i) for i in mapid])
                database.write(strid)
                database.write("\n")
        else:
            t = self.get_database()
            for i in range(len(t)):
                if t[i]['tour_id'].replace("\n", "") == self.tour_id:
                    t[i]['maps'] += [self._get_str_map_id_(i) for i in mapid]
            self._write_db_for_dict_arr(t)
    
    @staticmethod
    def _write_db_for_dict_arr(arr):
        with open('db.mph', 'w+') as database:
            for i in arr:
                database.write(i['tour_id'].replace("\n", ""))
                database.write("\n")
                database.write("&&&".join(i['maps']).replace("\n", ""))
                database.write("\n")