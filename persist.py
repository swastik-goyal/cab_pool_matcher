import json
import os
import heapq
from classes import RideRequest

STATE_FILE = 'state.json'


def request_to_dict(r):
    return {"name": r.name, "destination": r.destination, "when": r.when,
            "year": r.year, "when_requested": r.when_requested, "seq": r.seq}


def dict_to_request(d):
    r = RideRequest(d["name"], d["when_requested"])
    r.set_destination(d["destination"])
    r.set_when(d["when"])
    r.set_year(d["year"])
    r.seq = d["seq"]
    return r


def save_state(cabs, requests, next_seq):
    state = {"next_seq": next_seq, "cabs": [], "waiting": []}

    for cab in cabs:
        state["cabs"].append({"driver_name": cab.driver_name, "left": cab.left,
                              "students": [request_to_dict(s) for s in cab.students]})

    for heap in requests.values():
        for item in heap:
            state["waiting"].append(request_to_dict(item[3]))

    # write to a temp file first so a crash doesnt break the old save
    with open(STATE_FILE + ".tmp", "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)
    os.replace(STATE_FILE + ".tmp", STATE_FILE)


def load_state(cabs):
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, encoding="utf-8") as file:
        state = json.load(file)

    if len(state["cabs"]) != len(cabs):
        raise ValueError("saved cabs dont match cabs.csv")

    left_list = []
    students_list = []
    for saved, cab in zip(state["cabs"], cabs):
        if saved["driver_name"] != cab.driver_name:
            raise ValueError("saved cabs dont match cabs.csv")
        students = [dict_to_request(s) for s in saved["students"]]
        if len(students) > cab.seats:
            raise ValueError("too many students in a cab")
        left_list.append(saved["left"])
        students_list.append(students)

    requests = {}
    for d in state["waiting"]:
        r = dict_to_request(d)
        requests.setdefault((r.destination, r.when), []).append((-r.year, r.when_requested, r.seq, r))
    for heap in requests.values():
        heapq.heapify(heap)

    for i, cab in enumerate(cabs):
        cab.left = left_list[i]
        cab.students = students_list[i]

    return requests, int(state["next_seq"])
