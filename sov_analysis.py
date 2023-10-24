from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd


class StackoverflowSurvey:

    def __init__(self, df=None, keep_cols=None, year=None) -> None:
        if df is None:
            raise ValueError("DataFrame cannot be empty")
        
        df.dropna(axis='index', how='any', subset=['DevType', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'YearsCodePro', 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith', 'VersionControlSystem', 'ConvertedCompYearly'], inplace=True)

        self.year = year
        self.df =df
        self.cols = df.columns

        if keep_cols is not None:
            self.cols = keep_cols
            self.df = df.drop(columns=[column for column in df.columns if column not in keep_cols], axis=1)
            self.df.dropna(axis='index', how='any', inplace=True)
        
        self.rows = self.df.shape[0]


    def unique_set(self, colname, sep=';') -> set:
        """
        This method returns unique set of all values in a multi-valued column separated by 'sep'
        """
        unique_set = set()

        for row in self.df[colname].str.split(sep).values:
            unique_set.update(row)
        
        return sorted(unique_set)


    def distribution(self, colname, top=None, sep=';', perc=False, filter=None, exact_search=True, withsize=False) -> None:
        """
        This method returns a distribution of all values in a multi-valued column separated by 'sep'
        """
        counter = Counter()

        if filter is None:
            size = self.rows
        else:
            if exact_search:
                size = len([value for value in self.df[filter[0]].str.split(sep).values if filter[1] in value])
            else:
                size = self.rows if filter is None else self.df[self.df[filter[0]].str.contains(filter[1])].shape[0]

        # if exact_search and filter is not None:
        #     size = len([value for value in self.df[filter[0]].str.split(sep).values if filter[1] in value])
        # else:
        #     size = self.rows if filter is None else self.df[self.df[filter[0]].str.contains(filter[1])].shape[0]

        if filter is None:
            for row in self.df[colname].str.split(sep).values:
                counter.update(row)
        else:
            if exact_search:
                for index in self.df.index:
                    if filter[1] in self.df[filter[0]][index].split(sep):
                        counter.update(self.df[colname][index].split(sep))
                # for row in self.df[self.df[filter[0]].str.contains(filter[1])][colname].str.split(sep).values:
                #     counter.update(row)
            else:
                for row in self.df[self.df[filter[0]].str.contains(filter[1])][colname].str.split(sep).values:
                    counter.update(row)

        if perc:
            for key in counter.keys():
                    counter[key] = float(f"{(counter[key]/size)*100:.2f}")
        
        counter = sorted(counter.items(), key=lambda x:x[1], reverse=True)
        if top is not None:
            counter = counter[ : top+1]

        data = { key:value for key, value in counter }

        return (data, size) if withsize else data


    # def salary_distribution(self, colname, top=None, sep=';', filter=None, sal_col='ConvertedCompYearly', withsize=None, perc=False):
    def salary_distribution(self, colname, top=None, sep=';', perc=False, filter=None, exact_search=True, withsize=False, sal_col='ConvertedCompYearly'):
        """
        This method returns the salary distribution for values of specified column.
        """
        unique_set = self.unique_set(colname)
        salaries = { k:0 for k in unique_set}

        # Renaming C++ as CPP because + causes problems in regex
        # salaries['Cpp'] = salaries.pop('C++')

        if filter is None:
            for value in unique_set:
                for index in self.df.index:
                    if value in self.df[colname][index].split(sep):
                        salaries[value] += self.df[sal_col][index]
        else:
            for value in unique_set:
                for index in self.df.index:
                    if (value in self.df[colname][index].split(sep)) and (filter[1] in self.df[filter[0]][index].split(sep)):
                        salaries[value] += self.df[sal_col][index]

            # salaries[value] = self.df[self.df[colname].str.contains(value)][sal_col].sum()
            # print(salaries[value])

        if filter is None:
            size = self.rows
        else:
            if exact_search:
                size = len([value for value in self.df[filter[0]].str.split(sep).values if filter[1] in value])
            else:
                size = self.rows if filter is None else self.df[self.df[filter[0]].str.contains(filter[1])].shape[0]

        if perc:
            for key in salaries.keys():
                salaries[key] = float(f"{(salaries[key]/size)*100:.2f}")

        salaries = sorted(salaries.items(), key=lambda x:x[1], reverse=True)
        # print(salaries)
        if top is not None:
            salaries = salaries[ : top+1]
        
        data = { key:value for key, value in salaries }

        return (data, size) if withsize else data

        # return { key:value for key, value in salaries }


    def top_by(self, top, by, path=None) -> None:
        """
        TODO
        """
        topn = len(top)
        byn = len(by)

        for type1 in top:
            data1 = list(self.distribution(type1, perc=True, top=topn).keys())
            print('Type1:', data1)
            for type2 in by:
                data2 = list(self.distribution(type2, perc=True, top=byn, filter=(type1, data1)))
                print('Type2:', data2)

        '''
        for type1 in top:
            for type2 in by:
                data = self.counter(type1, perc=True, top=topn, filter=(type2, ''))
                print(data)
            print()
        '''


    def top_languages_by_devtypes(self, devtypes, top_langs=10, path=None) -> None:
        """
        
        """
        for devtype in devtypes:
            data = self.counter('LanguageHaveWorkedWith', perc=True, top=top_langs, filter=('DevType', devtype))
            print(data)




    def top_devtypes_by_languages(self) -> None:
        """
        
        """
        pass


    def top_webframeworks_by_devtypes(self) -> None:
        """
        
        """
        pass

    @staticmethod
    def visualize_distribution(data, size=None, xlabel='X-Axis', ylabel='Y-Axis', path=None, title=None, perc=True, dpi=300, style='seaborn'):
        """
        Method to visualize data.
        Note that if values seem to be incorrect, make sure that 'perc' for counter() is False
        :param data: Should be dictionary
        """

        # To improve quality of graphs. Source - https://blakeaw.github.io/2020-05-25-improve-matplotlib-notebook-inline-res/
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300

        x = list(data.keys())[::-1]
        y = list(data.values())[::-1]

        if size is not None and perc:
            for i in range(len(x)):
                x[i] = f"{x[i]} {(y[i]/size)*100:.2f}% "

        plt.style.use(style)
        plt.barh(x, y)
        plt.title('Data' if title is None else title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        if path is not None:
            plt.savefig(path, dpi=dpi)
        plt.show()



if __name__ == '__main__':
    df = pd.read_csv('data/survey_results_public-2022.csv')
    sov = StackoverflowSurvey(df, keep_cols=['DevType', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'YearsCodePro', 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith', 'VersionControlSystem', 'ConvertedCompYearly'])
    print()
    # print(sov.unique_set(colname='DevType'))
    # print()
    # print(sov.unique_set(colname='LanguageHaveWorkedWith'))
    # print()
    # print(sov.unique_set(colname='WebframeHaveWorkedWith'))
    # print()
    # print(sov.counter(colname='DevType'))
    # print(len(sov.counter(colname='DevType', top=5)))
    # print()
    # print(sov.counter(colname='LanguageHaveWorkedWith'))
    # print()
    # print(sov.counter(colname='WebframeHaveWorkedWith'))

    # sov.counter('DevType', perc=True, top=5, filter=('LanguageHaveWorkedWith', 'Python'))
    # {
    #     'Developer, back-end': 43.54,
    #     'Developer, full-stack': 42.06,
    #     'Developer, front-end': 20.02,
    #     'Developer, desktop or enterprise applications': 13.89,
    #     'Student': 13.42,
    #     'DevOps specialist': 12.57
    # }
    # sov.counter('DevType', perc=True, top=5, filter=('LanguageHaveWorkedWith', 'Python')) 
    # {
    #     'Developer, back-end': 38.56,
    #     'Data scientist or machine learning specialist': 23.61,
    #     'Engineer, data': 11.58,
    #     'Academic researcher': 10.12,
    #     'Developer, full-stack': 9.53,
    #     'Data or business analyst': 8.65
    # }

    # sov.counter('DevType', perc=True, top=5, filter=('LanguageHaveWorkedWith', 'Python')) 
    # {
        # 'Developer, back-end': 0.36,
        # 'Data scientist or machine learning specialist': 0.22,
        # 'Engineer, data': 0.11,
        # 'Academic researcher': 0.09,
        # 'Developer, full-stack': 0.09,
        # 'Student': 0.08
    # }
    # print(sov.counter('DevType', top=5))

    # data, size = sov.counter('LanguageHaveWorkedWith', top=15, withsize=True)
    # StackoverflowSurvey.visualize(data, size, xlabel='Percentage of people who want', ylabel='Language', path='languages.png', title='Most Popular Programming Languages', dpi=300)


    # Testing Salary Distribution

    #Testing without filter
    # sal_dist = sov.salary_distribution('LanguageHaveWorkedWith')
    # print(sal_dist['APL'] == df[df['LanguageHaveWorkedWith'].str.contains('APL')]['ConvertedCompYearly'].sum())
    # print(sal_dist['C++'] == df[df['LanguageHaveWorkedWith'].str.contains('C\+\+')]['ConvertedCompYearly'].sum()) # regex problem
    # print(sal_dist['Python'] == df[df['LanguageHaveWorkedWith'].str.contains('Python')]['ConvertedCompYearly'].sum())
    # print(sal_dist['JavaScript'] == df[df['LanguageHaveWorkedWith'].str.contains('JavaScript')]['ConvertedCompYearly'].sum())
    # # print(sal_dist['Java'] == df[df['LanguageHaveWorkedWith'].str.contains('Java')]['ConvertedCompYearly'].sum()) # JavaScript contains Java

    # Testing with filter
    # print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Blockchain'))['JavaScript'] == df.loc[(df['LanguageHaveWorkedWith'].str.contains('JavaScript')) & (df['DevType'].str.contains('Blockchain'))]['ConvertedCompYearly'].sum())
    # print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Developer, full-stack'))['Java'] == df.loc[(df['LanguageHaveWorkedWith'].str.contains('Java')) & (df['DevType'].str.contains('Developer, full-stack'))]['ConvertedCompYearly'].sum())
    # print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Developer, back-end'))['Python'] == df.loc[(df['LanguageHaveWorkedWith'].str.contains('Python')) & (df['DevType'].str.contains('Developer, back-end'))]['ConvertedCompYearly'].sum())
    # print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Scientist'))['Bash/Shell'] == df.loc[(df['LanguageHaveWorkedWith'].str.contains('Bash/Shell')) & (df['DevType'].str.contains('Scientist'))]['ConvertedCompYearly'].sum())
    # print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Marketing or sales professional'))['PHP'] == df.loc[(df['LanguageHaveWorkedWith'].str.contains('PHP')) & (df['DevType'].str.contains('Marketing or sales professional'))]['ConvertedCompYearly'].sum())

    print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Blockchain'), withsize=True, exact_search=False)[1] == df.loc[(df['DevType'].str.contains('Blockchain'))]['ConvertedCompYearly'].shape[0])
    print(sov.salary_distribution('LanguageHaveWorkedWith', filter=('DevType', 'Developer, full-stack'), withsize=True, exact_search=False)[1] == df.loc[ (df['DevType'].str.contains('Developer, full-stack'))]['ConvertedCompYearly'].shape[0])



    # print(sov.top_languages_by_devtypes(['Developer, full-stack', 'Student']))

