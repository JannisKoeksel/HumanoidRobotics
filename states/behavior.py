

from .state import State, StateMachine


idle = State("idle")
scanning = State("scanning")
defend = State("defend")
process_pwd = State("process_pwd")
check_identity = State("check_identity")
entry_approved = State("entry_approved")


idle >> scanning | "initialized"

scanning >> idle | "no_detection"
scanning >> check_identity | "motion"

check_identity >> process_pwd | "face_unknown"
check_identity >> entry_approved | "face_known"
check_identity >> scanning | "no_face"

process_pwd >> defend | "pwd_wrong"
process_pwd >> entry_approved | "pwd_correct"

defend >> scanning | "person_leaves"

entry_approved >> scanning | "waiting_for_entry"

