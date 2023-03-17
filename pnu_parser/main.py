import cse_parser
import pnu_parser
import recruit_parser


cse = cse_parser.CseParser()
cse.parseData()
cse.saveData()

pnu = pnu_parser.PnuParser()
pnu.parseData()
pnu.saveData()

recruit = recruit_parser.RecruitParser()
recruit.parseData()
recruit.saveData()