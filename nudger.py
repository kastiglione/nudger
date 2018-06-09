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

    # Evaluate the view expression using the language of the current function,
    # Swift or ObjC. The SBValue object return from EvaluateExpression() will
    # expose the view's address, which can be inserted in the below ObjC.
    view = frame.EvaluateExpression(viewExpression)

    # A value always has an error object, the `fail` property indicates when an
    # error actually occurred.
    if view.error.fail:
        result.SetError(view.error.description)
        return

    options = lldb.SBExpressionOptions()
    options.SetLanguage(lldb.eLanguageTypeObjC)

    # Import type info into lldb, otherwise lldb can't evaluate the ObjC below
    # without littering type casts throughout.
    frame.EvaluateExpression("@import UIKit", options)

    viewExpression = "(UIView *){}".format(view.value)
    nudgeExpression = """
        UIView *nudgedView = {viewExpression};
        nudgedView.frame = CGRectOffset(nudgedView.frame, {x}, {y});
        [CATransaction flush];
    """.format(viewExpression=viewExpression, x=x, y=y)

    error = frame.EvaluateExpression(nudgeExpression, options).error
    if error.fail and error.value != kNoResult:
        result.SetError(error.description)
        return
