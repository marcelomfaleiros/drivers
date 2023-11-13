import srs_sr830 as srs
sr830 = srs.LIA_SR830()
sr830.gpib_set_up()
sr830.initialize()
print(sr830.measure(2))
