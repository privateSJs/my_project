from roboflow import Roboflow

rf = Roboflow(api_key="sv9ITpmstUK9bDsAjk8x")
project = rf.workspace("jarekmasterdegree").project("master-degree-4utul")
version = project.version(1)
dataset = version.download("yolov8")
