# EE4-PostBotPat
HCR Coursework 2018

## Deadlines
- 1/11: Design Report
- 29/11: Individual Demo
- 13/12: Final Demo
- 20/12: Final Report

## Project Phases
- Phase 1: Can deal with medium sized packages, one person at a time, people only come when they have a package, printed labels. One package per person only.  
- Phase 2: Can have people arrive even if they don't have a package.
- Phase 3: Multiple packages per person allowed.
- Phase 4: Allow for more package sizes.

## Workflow
- New work (features, bug fixes etc.) begins life as an issue (e.g. implement time prediction for pick ups, fix mistaken identity bug).
- New code / assests are created in dev branches.
- A merge request is then opened to merge the dev branch into the integration branch.
- The integration branch is tested and evaluated.
- If testing is successful then the integration branch is merged into master and the issue is closed.

## How to run the Baxter simulation

In 2 terminal tabs, run:
```
cd ~/ros_ws

./baxter.sh sim
```

In the 1st tab, run:
```
roslaunch baxter_gazebo baxter_world.launch
```

The gazebo terminal window should open with the robot in the world.

Then, in the 2nd terminal tab:
```
rosrun baxter_tools enable_robot.py -e
```

You can now run python scripts to move Baxter and see it in the gazebo simulator. For example:
```
rosrun baxter_tools tuck_arms.py -t
```
