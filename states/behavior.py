

from .state import State, StateMachine


idle = State("idle")
scanning = State("scanning")
fight = State("fight")
defend = State("defend")
process_pwd = State("process_pwd")
entry_forbidden = State("entry_forbidden")
add_identity = State("add_identity")
check_identity = State("check_identity")
entry_approved = State("entry_approved")


idle >> scanning | "initialized"

scanning >> idle | "no_detection"
scanning >> check_identity | "motion"

check_identity >> entry_forbidden | "face_unknown"
check_identity >> entry_approved | "face_known"
check_identity >> scanning | "no_face"

entry_forbidden >> defend | "no_pwd"
entry_forbidden >> process_pwd | "has_pwd"

process_pwd >> defend | "pwd_wrong"
process_pwd >> add_identity | "pwd_correct"

add_identity >> idle | "identity_added"
add_identity >> idle | "person_leaves"

defend >> fight | "person_stays"
defend >> scanning | "person_leaves"

entry_approved >> idle | "waiting_for_entry"

fight >> idle | "person_leaves"





# StateMachine.print()

# print(StateMashie(idle).run())

