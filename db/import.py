from query import SitesQuery
from connect import Connect

session = Connect().get_session()
sites = SitesQuery(session)

sites.create(forestry='Сяськое', kvartal=153, vydel='10', clearcut=2000, planting=2001, thinning=2010)
sites.create(forestry='Сяськое', kvartal=153, vydel='12', clearcut=2000, planting=2001, thinning=2010)
sites.create(forestry='Пригородное', kvartal=184, vydel='10', clearcut=2000, planting=2001, thinning=2010)
sites.create(forestry='Шомушское', kvartal=77, vydel='10', clearcut=2000, planting=2001, thinning=2011)
