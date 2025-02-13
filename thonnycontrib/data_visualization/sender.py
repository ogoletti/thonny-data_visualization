from thonny import get_runner
from thonny.common import InlineCommand

def send(self):
    if (self.var_to_request["globals"]):
        var = next(iter(self.var_to_request["globals"]))
        object_id = self.var_to_request["globals"][var].id
        self.parent_id = "Globals"
        del self.var_to_request["globals"][var]

    elif (self.var_to_request["locals"]):
        var = next(iter(self.var_to_request["locals"]))
        object_id = self.var_to_request["locals"][var].id
        self.parent_id = "Locals"
        del self.var_to_request["locals"][var]
    
    elif (self.name != "GV" and self.var_to_request["lazy"]):
        var = next(iter(self.var_to_request["lazy"]))
        object_id = self.var_to_request["lazy"][var].id
        self.parent_id = self.lazy_id
        del self.var_to_request["lazy"][var]

    else:
        parent = next(iter(self.var_to_request["children"]))
        var = next(iter(self.var_to_request["children"][parent]))
        if (var == "..."):
            self.add_next(parent, var)
            del self.var_to_request["children"][parent][var]
            if (len(self.var_to_request["children"][parent]) == 0):
                del self.var_to_request["children"][parent]
            self.send_request()
            return
        object_id = self.var_to_request["children"][parent][var].id
        self.parent_id = parent
        del self.var_to_request["children"][parent][var]
        if (len(self.var_to_request["children"][parent]) == 0):
            del self.var_to_request["children"][parent]

    assert object_id is not None
    self.object_id = object_id
    self.object_name = var
    self.iter += 1
    get_runner().send_command(InlineCommand(
            "get_object_info",
            id = 'NT ' + str(self.iter),
            object_id=self.object_id,
            include_attributes=True,
            all_attributes=False
        )
    )

def fast_send(self):
    get_runner().send_command(InlineCommand(
            "get_object_info",
            id = self.name + ' ' + str(self.iter),
            object_id=self.object_id,
            include_attributes=True,
            all_attributes=False
        )
    )