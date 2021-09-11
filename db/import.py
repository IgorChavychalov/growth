from query import SitesQuery, PlotsQuery
from db.connect import Connect

session = Connect().get_session()
sites = SitesQuery(session)
plots = PlotsQuery(session)

sites.create(forestry='Сяськое', kvartal=153, vydel='10', clearcut=2000, planting=2001, thinning=2010)
sites.create(forestry='Сяськое', kvartal=154, vydel='12', clearcut=2000, planting=2001, thinning=2010)
sites.create(forestry='Пригородное', kvartal=184, vydel='10', clearcut=2000, planting=2001, thinning=2010)
sites.create(forestry='Шомушское', kvartal=77, vydel='10', clearcut=2000, planting=2001, thinning=2011)

plots.create(id_site=1, TLU="С2", forest_type="ЧС", number=1, area=600)
plots.create(id_site=1, TLU="С2", forest_type="ЧС", number=2, area=600)
plots.create(id_site=1, TLU="С2", forest_type="ЧС", number=3, area=600)

plots.create(id_site=2, TLU="С2", forest_type="ЧС", number=1, area=600)
plots.create(id_site=2, TLU="С2", forest_type="ЧС", number=2, area=600)
plots.create(id_site=2, TLU="С2", forest_type="ЧС", number=3, area=600)

plots.create(id_site=3, TLU="С3", forest_type="ЧВ", number=1, area=800)
plots.create(id_site=3, TLU="С3", forest_type="ЧВ", number=2, area=800)

plots.create(id_site=3, TLU="В3", forest_type="ДЛ", number=1, area=800)
plots.create(id_site=3, TLU="В3", forest_type="ДЛ", number=2, area=800)

tax