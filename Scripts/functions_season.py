import pandas as pd


class season_data:

    def __init__(self, data):
        self.seasons = ['summer', 'autumn', 'winter', 'spring']
        self.data = data
        self.days = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
        }

    def calc_hourly_day_mean(self):
        days_names = [self.days[day] for day in self.days]
        self.hourly_day_mean = pd.DataFrame(index=[i for i in range(24)],
                                            columns=days_names)
        for day in self.days:
            data_days = self.data.loc[self.data.index.weekday == day]
            self.hourly_day_mean[self.days[day]] = data_days.groupby(
                data_days.index.hour).mean()

    def calc_hourly_season_mean(self):
        self.calc_season_data()
        self.hourly_season_mean = pd.DataFrame(index=[i for i in range(24)],
                                               columns=self.seasons)
        for season in self.seasons:
            data_season = self.obtain_season_data(season)
            self.hourly_season_mean[season] = data_season.groupby(
                data_season.index.hour).mean()

    def calc_season_data(self):
        self.decision_season = pd.DataFrame(index=self.data.index,
                                            columns=self.seasons)
        dates = self.data.index.astype("str").str[5:10]
        self.decision_season["spring"] = (dates >= '03-20') & (dates < '06-21')
        self.decision_season["summer"] = (dates >= '06-21') & (dates < '09-23')
        self.decision_season["autumn"] = (dates >= '09-23') & (dates < '12-21')
        self.decision_season["winter"] = (dates >= '12-21') | (dates < '03-20')

    def obtain_season_data(self, season):
        return self.data.loc[self.decision_season[season]]
