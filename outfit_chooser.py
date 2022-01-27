import random as r

class Outfit:

    top1 = None
    top2 = None
    bottom = None
    footwear = None
    coat = None

    def __init__(self,cold,wind,rain):
        self.cold = cold
        self.wind = wind
        self.rain = rain


    def choose_outfit(self,style,wardrobe):
        
        #Start with footwear
        f_rows = wardrobe.loc[wardrobe['Type'] == 'Footwear']
        self.footwear = r.choice(f_rows.index)
        # Now pants and top 1
        if(style == 'Classy-casual'):
            b_rows = wardrobe.loc[(wardrobe['Type'] == 'Bottom') & 
                                       ((wardrobe['Style'] == 'Classy-casual') | (wardrobe['Style'] == 'Casual'))]
            self.bottom = r.choice(b_rows.index)
            t1_rows = wardrobe.loc[(wardrobe['Type'] == 'Top') & 
                                        ((wardrobe['Style'] == 'Classy-casual') | (wardrobe['Style'] == 'Classy'))]
            self.top1 = r.choice(t1_rows.index)
        else:
            b_rows = wardrobe.loc[(wardrobe['Type'] == 'Bottom')]
            t1_rows = wardrobe.loc[wardrobe['Type'] == 'Top']
            self.bottom = r.choice(b_rows.index)
            self.top1 = r.choice(t1_rows.index)
        
        # Top2
        if (wardrobe.at[self.top1, 'Cold'] == 0 and self.cold == 1):
            if(style == 'Classy-casual'):
                t2_rows = wardrobe.loc[(wardrobe['Type'] == 'Top') & 
                                            (wardrobe['Cold'] == 1) & 
                                            ((wardrobe['Style'] == 'Classy-casual') | (wardrobe['Style'] == 'Classy'))]
                self.top2 = r.choice(t2_rows.index)
            else:
                t2_rows = wardrobe.loc[(wardrobe['Type'] == 'Top') & 
                                            (wardrobe['Cold'] == 1)]
                self.top2 = r.choice(t2_rows.index)
        if (self.rain == 1) or (self.wind == 1):
            c_rows = wardrobe.loc[wardrobe['Type'] == 'Outer']
            self.coat = r.choice(c_rows.index)

        return None
    
    def change_items(self,curr_outfit,answers,wardrobe):
        for i in range(len(answers)):
            if answers[i][0].get():
                clothing_type = curr_outfit.iloc[i]['Type']
                rows = wardrobe.loc[(wardrobe['Type'] == clothing_type) & 
                                    (wardrobe['Style'] == curr_outfit.iloc[i]['Style']) &
                                    (wardrobe['ID'] != curr_outfit.iloc[i]['ID'])]
                new_item = r.choice(rows.index)
                curr_outfit.iloc[i] = wardrobe.iloc[new_item]
        return curr_outfit