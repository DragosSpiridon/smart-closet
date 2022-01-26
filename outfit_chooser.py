import random as r

class Outfit:

    top1 = None
    top2 = None
    bottom = None
    footwear = None
    coat = None

    def __init__(self,cold,wind,rain,wardrobe):
        self.cold = cold
        self.wind = wind
        self.rain = rain
        self.wardrobe = wardrobe


    def choose_outfit(self,style):
        
        #Start with footwear
        f_rows = self.wardrobe.loc[self.wardrobe['Type'] == 'Footwear']
        self.footwear = r.choice(f_rows.index)
        # Now pants and top 1
        if(style == 'Classy-casual'):
            b_rows = self.wardrobe.loc[(self.wardrobe['Type'] == 'Bottom') & 
                                       ((self.wardrobe['Style'] == 'Classy-casual') | (self.wardrobe['Style'] == 'Casual'))]
            self.bottom = r.choice(b_rows.index)
            t1_rows = self.wardrobe.loc[(self.wardrobe['Type'] == 'Top') & 
                                        ((self.wardrobe['Style'] == 'Classy-casual') | (self.wardrobe['Style'] == 'Classy'))]
            self.top1 = r.choice(t1_rows.index)
        else:
            b_rows = self.wardrobe.loc[(self.wardrobe['Type'] == 'Bottom')]
            t1_rows = self.wardrobe.loc[self.wardrobe['Type'] == 'Top']
            self.bottom = r.choice(b_rows.index)
            self.top1 = r.choice(t1_rows.index)
        
        # Top2
        if (self.wardrobe.at[self.top1, 'Cold'] == 0 and self.cold == 1):
            if(style == 'Classy-casual'):
                t2_rows = self.wardrobe.loc[(self.wardrobe['Type'] == 'Top') & 
                                            (self.wardrobe['Cold'] == 1) & 
                                            ((self.wardrobe['Style'] == 'Classy-casual') | (self.wardrobe['Style'] == 'Classy'))]
                self.top2 = r.choice(t2_rows.index)
            else:
                t2_rows = self.wardrobe.loc[(self.wardrobe['Type'] == 'Top') & 
                                            (self.wardrobe['Cold'] == 1)]
                self.top2 = r.choice(t2_rows.index)
        if (self.rain == 1) or (self.wind == 1):
            c_rows = self.wardrobe.loc[self.wardrobe['Type'] == 'Outer']
            self.coat = r.choice(c_rows.index)

        return None
    
    def change_items(self,curr_outfit,answers):
        
        for i in range(len(answers)):
            
            if answers[i][0].get():
                clothing_type = curr_outfit.iloc[i]['Type']
                rows = self.wardrobe.loc[(self.wardrobe['Type'] == clothing_type) & 
                                         (self.wardrobe['Style'] == curr_outfit.iloc[i]['Style']) &
                                         (self.wardrobe['Cold'] == curr_outfit.iloc[i]['Cold']) &
                                         (self.wardrobe['Wind'] == curr_outfit.iloc[i]['Wind']) &
                                         (self.wardrobe['Rain'] == curr_outfit.iloc[i]['Rain']) &
                                         (self.wardrobe['ID'] != curr_outfit.iloc[i]['ID'])]
                new_item = r.choice(rows.index)
                curr_outfit.iloc[i] = self.wardrobe.iloc[new_item]


        return curr_outfit