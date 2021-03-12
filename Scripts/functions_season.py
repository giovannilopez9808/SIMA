import pandas as pd


class season_data:

    def __init__(self, data):
        self.seasons = ['summer', 'autumn', 'winter', 'spring']
        self.data = data

    def calc_hourly_day_mean(self):
        days = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
        }
        days_names = [days[day] for day in days]
        self.data = pd.DataFrame(columns=days_names)
        for day in days:
            self.data[days[day]] = self.data.loc[self.data.index.weekday == day]

    def calc_hourly_season_mean(self):
        self.obtain_season_data(self)
        self.data_season = self.data_season.groupby(
            self.data_season.index.hour).mean()

    def calc_season_data(self):
        self.decision_season = pd.DataFrame(columns=self.seasons)
        dates = self.data.index.astype("str").str[5:10]
        self.decision_season["spring"] = (dates >= '03-20') & (dates < '06-21')
        self.decision_season["summer"] = (dates >= '06-21') & (dates < '09-23')
        self.decision_season["autumn"] = (dates >= '09-23') & (dates < '12-21')
        self.decision_season["winter"] = (dates >= '12-21') | (dates < '03-20')
        self.decision_season.index = self.data.index

    def obtain_season_data(self, season):
        return self.data.loc[self.decision_season[season]]
