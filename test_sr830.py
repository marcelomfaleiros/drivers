import srs_sr830 as srs
sr830 = srs.LIA_SR830()
sr830.gpib_set_up()
sr830.initialize()
sr830.measure(1)
#sr830.reset()
