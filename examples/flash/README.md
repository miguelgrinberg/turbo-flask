# Flash

This example demonstrates how to flash a message when responding to a form submission with a turbo-stream response.

The turbo-stream response includes the specific parts of the page that need to be updated, so calling `flash()` to display an alert does not have any effect unless the alert section of the page is included in the list of updates.

The solution presented in this example uses an `after_request` handler that adds an additional stream update with the flashed messages when the response is detected to be a turbo-stream response.
