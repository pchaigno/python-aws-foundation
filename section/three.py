# -*- coding : utf8 -*-


class SectionThree:

    def __init__(self, CT, CW):
        self.CT = CT
        self.CW = CW

    def section_3_1(self):
        self.name = "3.1 Ensure a log metric filter and alarm exist for unauthorized API calls"
        self.scored = True
        self.passed = True
        for row in self.CT.trailsReport:
            if "CloudWatchLogsLogGroupArn" in row:
                group_name = row["CloudWatchLogsLogGroupArn"].split(":")[-2]
                self.CW.logGroupName = group_name
                metrics = self.CW.getMetricFilters(group_name)
                if metrics["metricFilters"]:
                    for metric in metrics["metricFilters"]:
                        print(metric)
                else:
                    self.passed = False
            else:
                self.scored = False
        print("{}, passed : {}".format(self.name, self.passed))

    def cis_check(self):
        self.section_3_1()
