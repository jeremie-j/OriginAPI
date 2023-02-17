import json

with open('./scripts/scrap_mapping/mapping.json', 'r') as outfile:
    outfile_data = json.load(outfile)

print("\nLegends : \n")
for legend in sorted(list(outfile_data['legends'].keys())):
    print(legend + "=" + str(outfile_data['legends'][legend]["legend_id"]))


for legend in sorted(list(outfile_data['legends'].keys())):
    print(f'Writing file for {legend}')

    legend_trackers = outfile_data['legends'][legend]["trackers"].items()
    legend_skins = outfile_data['legends'][legend]["skins"].items()
    legend_intros = outfile_data['legends'][legend]["intros"].items()
    legend_frames = outfile_data['legends'][legend]["frames"].items()
    legend_badges = outfile_data['legends'][legend]["badges"].items()
    with open(f"./schemas/legends/{legend.lower().replace(' ','_')}.py", "w") as f:
        f.write(f"legend_name = '{legend.lower().replace(' ','_')}'\n")
        f.close()
    variable = 'trackers = {'
    for tracker_id, tracker_name in legend_trackers:
        variable += (str(tracker_id) +
                     ":{\"name\":\""+tracker_name+"\"},")
    variable += "}\n"

    variable = variable + 'badges = {'
    for badge_id, badge_name in legend_badges:
        variable += (str(badge_id) +
                     ":{\"name\":\""+badge_name+"\"},")
    variable += "}\n"

    variable += 'skins = {'
    for skin_id, skin_name in legend_skins:
        variable += (str(skin_id) +
                     ":{\"name\":\""+skin_name+"\"},")
    variable += "}\n"

    variable += 'frames = {'
    for frame_id, frame_name in legend_frames:
        variable += (str(frame_id) +
                     ":{\"name\":\""+frame_name+"\"},")
    variable += "}\n"

    variable += 'intros = {'
    for intro_id, intro_name in legend_intros:
        variable += (str(intro_id) +
                     ":{\"name\":\""+intro_name+"\"},")
    variable += "}\n"
    with open(f"./schemas/legends/{legend.lower().replace(' ','_')}.py", "a") as f:
        f.write(variable)
