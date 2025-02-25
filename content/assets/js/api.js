async function handleApiRequest(button, confirmationMessage) {
    // make button submitting
    var originalText = button.text();
    button.text("Submitting...").prop("disabled", true);

    var confirmUpdate = true;
    console.log(confirmationMessage);
    if (confirmationMessage) {
        confirmUpdate = confirm(confirmationMessage);
    }
    if (confirmUpdate) {
//        var requireValidation = button.data("check-validation");
         var validationFunctionName = button.data("validation-function");
         if (validationFunctionName) {
            // Call the validation function defined in the HTML page
            if (typeof window[validationFunctionName] === 'function') {
                var validationErrors = window[validationFunctionName]();
                if (validationErrors) {
                // Validation failed, do not proceed with the AJAX request
                return;
                }
            } else {
                console.error("Validation function not found: " + validationFunctionName);
            }

        }

        var requestData;
        if (button.data('type') === "form") {
            // If the button is specified as a form button
            var form = button.closest("form");
            if(!$(form[0]).valid()){
                button.text(originalText).prop("disabled", false);
                return false;
            }
            requestData = form.serialize();
        } else if (button.data('type') === "formFile") {
            // If the button is specified as a form button with a file input
            var form = button.closest("form");
            requestData = new FormData(form[0]);
        } else {
            // If it's not a form button, use custom data attribute for requestData
            requestData = button.data("data");
        }
        var url = button.data("url");
        var method = button.data("method");
        var successMessage = button.data("success-message");
        var errorMessage = button.data("error-message");
        var onSuccess = button.data("on-success");
        var onFailure = button.data("on-failure");
        var showPopup = button.data("show-popup");

        // wait for confirmation
        var confirmTypeToText = button.data("type-confirm");
        if (confirmTypeToText) {
          try {
            await confirmWithText(confirmTypeToText);
          } catch (error) {
            button.text(originalText).prop("disabled", false);
            return false;
          }
        }


        var ajaxOptions = {
            url: url,
            type: method,
            data: requestData,
            success: function(returnedData) {

                console.log("Response type: " + typeof returnedData.response); // Check the type of response
                console.log("Response value: " + returnedData.response); // Log the response value
                button.text(originalText).prop("disabled", false);
                if (returnedData.response == '1') {
                    var successMessageToDisplay = returnedData.message || successMessage || "Operation successful.";
                    if (showPopup) {
                        alert(successMessageToDisplay);
                    }
                    if (typeof window[onSuccess] === 'function') {
                        window[onSuccess](returnedData, button);
                    }
                    else{
                        location.reload();
                    }
                } else {
                    var errorMessageToDisplay = returnedData.error || errorMessage || "Operation failed.";
                    if (showPopup) {
                        alert(errorMessageToDisplay);
                    }
                    if (typeof window[onFailure] === 'function') {
                        window[onFailure](returnedData, button);
                    }
                }
            },
            error: function(xhr, status, error) {
                button.text(originalText).prop("disabled", false);
                var errorMessageToDisplay = errorMessage || xhr.responseJSON.error || "Operation failed.";
                if (showPopup) {
                    alert(errorMessageToDisplay);
                }
                if (typeof window[onFailure] === 'function') {
                    window[onFailure](xhr.responseJSON || error, button);
                }
            }


        };
        // Adjust options for FormData
        if (button.data('type') === "formFile") {
            ajaxOptions.processData = false;
            ajaxOptions.contentType = false;
        }
        $.ajax(ajaxOptions);
    }
    button.text(originalText).prop("disabled", false);
    return false;
}
$(document).ready(function() {
    $(".api-action").click(function() {
        var confirmationMessage = $(this).data("confirmation-message");
        // console.log(confirmationMessage);
        handleApiRequest($(this), confirmationMessage);
        return false;
    });
});

function showFormError(returnedData, button) {
    // Find the nearest form using the button
    var $form = $(button).closest('form');

    // Find the element with class 'form-messages' within the form
    var $formMessages = $form.find('.form-messages');
    // If there's an error in the returned data
    if (returnedData.errors) {
        // Display the error message in the 'form-messages' element
        if (typeof returnedData.errors == 'object') {
            // Convert JSON object to a formatted string with 2-space indentation
            var errorString = JSON.stringify(returnedData.errors, null, 2);

            // Display the formatted JSON string in the $formMessages element

            $formMessages.text(errorString);
        } else {
            // If it's not an object, just set the text directly
            $formMessages.text(returnedData.errors);
        }
        // Optionally, you can add a class to indicate an error state (if needed)
        $formMessages.addClass('text-danger');
    } else {
        // If no error, clear the 'form-messages' content
        $formMessages.text('');
        $formMessages.removeClass('text-danger');
    }
}

function confirmWithText(inputText) {
  return new Promise((resolve, reject) => {
    // Create and show the modal
    const modalHtml = `
      <div class="modal fade" id="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content" style="background-color: #fff; color: #000; border-radius: 8px;">
            <div class="modal-header" style="border-bottom: 1px solid #ddd;">
              <h5 class="modal-title" id="confirmModalLabel">Delete ${inputText}?</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="color: #ffcc00; font-size: 1.5rem; margin-right: 10px;">&#9888;</span>
                <div>
                  <strong>Warning:</strong> Deleting your data will result in permanent data loss.
                </div>
              </div>
              <p>To confirm deletion, type the name (<strong>${inputText}</strong>) in the field below:</p>
              <input type="text" id="confirmationInput" class="form-control" placeholder="Enter Label" style="border: 1px solid #ddd; margin-top: 10px;" />
              <p style="font-size: 0.9rem; margin-top: 10px;">
                To disable type-to-confirm, go to the Type-to-Confirm section of
                <a href="/setting" style="color: #007bff;">My Settings</a>.
              </p>
            </div>
            <div class="modal-footer d-flex justify-content-end">
              <button type="button" id="confirmButton" class="btn btn-primary me-2">Confirm</button>
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    `;

    // Append the modal to the body
    $('body').append(modalHtml);

    // Initialize and show the modal using Bootstrap's modal methods
    var modal = new bootstrap.Modal(document.getElementById('confirmModal'), {
      backdrop: 'static', // Prevent closing the modal by clicking outside of it
      keyboard: false // Disable closing the modal with the keyboard
    });
    modal.show();

    // Handle the confirmation button click
    $('#confirmButton').click(function () {
      var userInput = $('#confirmationInput').val();
      if (userInput === inputText) {
        modal.hide();
        $(this).remove();
        resolve(); // Resolve the promise when the correct text is entered
      } else {
        alert('The text you entered does not match. Please try again.');
      }
    });

    // Handle the cancel button click or modal close
    $('#confirmModal').on('hidden.bs.modal', function () {
      $(this).remove();
      reject(); // Reject the promise if the modal is closed or canceled
    });
  });
}