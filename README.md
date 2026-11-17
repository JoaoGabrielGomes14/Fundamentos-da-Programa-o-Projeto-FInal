Final project for programming:

Build 4 scenarios and a main menu.
Explanation:

--- we want to make it modular and use object oriented programming principles. Right now we will have one json(config/config.json) file holding all the information about windows or buttons or anything we might need in the future, for example phisical entities. All data should live in this file, we do not want to have random magical numbers and info around the program. the loader module should be encharged of retrieving info from the config file so it can be used. The info right is organized by scenarios, where the main menu is also a scenario.

---We want to have strongly typed objects encharded of representing everything in the program. to be able to keep the modularity we want to use  the types defined in  types_config. The loader gives an object scenario that has itself custom object holding all info on the scenario. For example the window holds a window settings object that holds all info needed to create a windows, and can also create that window. 

---Types until now (update later) we have like said the scenario , we need to still choose btw if we will make this with dependency injection or with SLP (to me feels more natural since then each scenario is truly independent), we have the button settings that will serve to create buttons(which are custom objects since graphics-py does not have buttons) in that we have buttons style which just serves to be able to have a "deafualt" style in case we dont wrtie it in the json.

---the graphical_logic particulary classes will  mainly be used to represent custom graphics, anything from the button to potentially(if we have time) animations.

---the first menu is special in that it is also somewhat responsibvle to calling the others , we can chooose if we make the logic there or if we differ and write a custom orchestrator , might be better. 


Notes:
i think we should leave the "pretty graphics" to the end, with this architecture its very very easy and risk free to change graphis so lets just make an MVP and move on.

right now, and probably for a while this will be super fragile in that a single error will wipe everything, we need to chose if we go slow now and then when its finished try our best to break everything or if we go slowly doing it

same applies to logging errors and or state
