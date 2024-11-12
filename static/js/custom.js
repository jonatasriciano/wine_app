// static/js/winePreferenceForm.js
$(document).ready(function () {
    let currentStep = 1;
    const totalSteps = $(".step").length;

    function showStep(step) {
        $(".step").hide();
        $(`.step[data-step="${step}"]`).show();
    }

    function validateStep(step) {
        const $step = $(`.step[data-step="${step}"]`);
        let isValid = true;

        $step.find("input, select, textarea").each(function () {
            if (this.type === "radio") {
                const name = $(this).attr("name");
                if ($(`input[name="${name}"]:checked`).length === 0) {
                    $(this).closest(".step").find(".error-msg").text("Please select an option.");
                    isValid = false;
                } else {
                    $(this).closest(".step").find(".error-msg").text("");
                }
            } else {
                if (!this.checkValidity()) {
                    $(this).addClass("is-invalid");
                    $(this).next(".error-msg").text(this.validationMessage);
                    isValid = false;
                } else {
                    $(this).removeClass("is-invalid");
                    $(this).next(".error-msg").text("");
                }
            }
        });
        return isValid;
    }

    $(".next-button").on("click", function () {
        if (validateStep(currentStep) && currentStep < totalSteps) {
            currentStep++;
            showStep(currentStep);
        }
    });

    $(".prev-button").on("click", function () {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    $("#winePreferenceForm").on("submit", function (e) {
        if (!validateStep(currentStep)) {
            e.preventDefault();
            alert("Please complete all fields correctly before submitting.");
        }
    });

    showStep(currentStep);

    const $slider = $("#id_budget");
    const $output = $("#budget_value span");
    $output.text($slider.val());

    $slider.on("input", function() {
        $output.text($(this).val());
    });

    const $grapeRegionSelect = $("#id_grape_region");
    if ($grapeRegionSelect.length) {
        $grapeRegionSelect.BsMultiSelect();
    }
});