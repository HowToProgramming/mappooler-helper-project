from start import osu, atr

class sheet():
    def __init__(self, sheeturl, index, mappooler, mappooleramt):
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
        self.worksheet.update_cell(row, 4, t)
        self.worksheet.update_cell(row, 5, comments)
    
    def vote(self, beatmapid, statement):
        self.update_sheet()
        if statement == True:
            statement = 1
        elif statement == False:
            statement = 0
        row = 0; col = 0
        for i in self.val:
            row += 1
            if i[1].split("/")[-1] == str(beatmapid):
                break
        for bruh in self.val[0]:
            col += 1
            if bruh == self.mappooler:
                break
        self.worksheet.update_cell(row, col, statement)
    
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


        
    # nice --- "e^iz = isinz + cosz" b64---b25lIHplcm8gZWlnaHQgc2V2ZW4gbmluZSBzaXggemVybyB6ZXJv---
    def checkAgreement(self):
        self.update_sheet()
        agreement = []
        # 5 6 7 8 df2+1
        for i in range(len(self.val)):
            sumagreement = 0
            for j in range(5,5 + self.mappooleramt):
                if i == 0:
                    continue
                if self.val[i][j] == 'TRUE':
                    sumagreement += 1
                    continue
                if self.val[i][j] == "FALSE":
                    continue
                try:
                    sumagreement += int(self.val[i][j])
                except:
                    continue
            if(sumagreement >= self.mappooleramt // 2):
                agreement.append(int(self.val[i][1].split("/")[-1]))
        return agreement

    def pickAgreement(self):
        self.update_sheet()
        for i in self.checkAgreement():
            self.pick(i)
    
    def showAllMaps(self):
        self.update_sheet()
        beatmapsid = []
        type_ = []
        for i in self.val:
            if i == self.val[0]:
                continue
            beatmapsid.append(i[1].split("/")[-1])
            type_.append(i[3])
        str_beatmap_data = ""
        for i in range(len(beatmapsid)):
            try:
                bmdata = osu.beatmaps(beatmapsid[i])
                str_beatmap_data += "[{}] {} - {} [{}] - https://osu.ppy.sh/b/{}\n".format(type_[i], bmdata['artist'], bmdata['title'], bmdata['version'], beatmapsid[i])
            except:
                pass
        return str_beatmap_data