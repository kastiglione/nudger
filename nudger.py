import lldb

# From UserExpression.h, "returns this if there is no result"
kNoResult = 0x1001

@lldb.command("nudger")
def nudger(debugging, input, context, result, _):
    # type: (lldb.SBDebugger, str, lldb.SBExecutionContext, lldb.SBCommandReturnObject, dict) -> None
    frame = context.frame

    args = input.split(" ", 2)
    if len(args) != 3:
        result.SetError("Usage: nudger x y view")
        return

    (x, y, viewExpression) = args

    # Import type info into lldb, otherwise lldb can't evaluate the ObjC
    # without the unconventional use of type casts.
    frame.EvaluateExpression("@import UIKit")

    nudgeExpression = """
        UIView *nudgedView = {viewExpression};
        nudgedView.frame = CGRectOffset(nudgedView.frame, {x}, {y});
        [CATransaction flush];
    """.format(viewExpression=viewExpression, x=x, y=y)

    error = frame.EvaluateExpression(nudgeExpression).error
    if error.fail and error.value != kNoResult:
        result.SetError(error.description)
        return
