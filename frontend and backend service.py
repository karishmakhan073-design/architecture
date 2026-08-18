// =====================================================
// RK HEALTH - FRONTEND
// =====================================================

const API_URL = CONFIG.SCRIPT_URL;


// =====================================================
// SEND REQUEST TO GOOGLE APPS SCRIPT
// =====================================================

async function sendRequest(action, data = {}) {

    try {

        const params = new URLSearchParams();

        params.append("action", action);

        Object.keys(data).forEach(key => {

            params.append(
                key,
                data[key] ?? ""
            );

        });


        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },

                body: params.toString()
            }
        );


        if (!response.ok) {

            throw new Error(
                "Backend request failed."
            );
        }


        const result =
            await response.json();


        return result;


    } catch (error) {

        console.error(
            "API Error:",
            error
        );

        return {
            success: false,
            status: error.message
        };
    }
}


// =====================================================
// ADD HEALTHCARE RECORD
// =====================================================

async function addLog() {

    const patientName =
        document
            .getElementById("patientName")
            .value
            .trim();

    const doctorName =
        document
            .getElementById("doctorName")
            .value
            .trim();

    const appointmentDate =
        document
            .getElementById("appointmentDate")
            .value;

    const appointmentTime =
        document
            .getElementById("appointmentTime")
            .value;

    const appointmentDetails =
        document
            .getElementById("appointmentDetails")
            .value
            .trim();

    const medication =
        document
            .getElementById("medication")
            .value
            .trim();

    const phoneNumber =
        document
            .getElementById("phoneNumber")
            .value
            .trim();

    const visitNotes =
        document
            .getElementById("visitNotes")
            .value
            .trim();


    // -----------------------------------------------
    // Frontend validation
    // -----------------------------------------------

    if (!patientName) {

        alert(
            "Patient name is required."
        );

        return;
    }


    if (!appointmentDate) {

        alert(
            "Appointment date is required."
        );

        return;
    }


    if (!appointmentTime) {

        alert(
            "Appointment time is required."
        );

        return;
    }


    if (!medication) {

        alert(
            "Medication information is required."
        );

        return;
    }


    if (!validatePhone(phoneNumber)) {

        alert(
            "Enter a valid phone number."
        );

        return;
    }


    // -----------------------------------------------
    // Send to backend
    // -----------------------------------------------

    const result = await sendRequest(
        "addLog",
        {
            patient_name:
                patientName,

            doctor_name:
                doctorName,

            appointment_date:
                appointmentDate,

            appointment_time:
                appointmentTime,

            appointment_details:
                appointmentDetails,

            medication_information:
                medication,

            phone_number:
                phoneNumber,

            visit_notes:
                visitNotes
        }
    );


    if (result.success) {

        alert(
            "Healthcare record added successfully."
        );

        document
            .getElementById("healthForm")
            .reset();

    } else {

        alert(
            result.status ||
            "Unable to save record."
        );
    }
}


// =====================================================
// PHONE VALIDATION
// =====================================================

function validatePhone(phone) {

    const pattern =
        /^\+?[1-9]\d{9,14}$/;

    return pattern.test(phone);
}


// =====================================================
// GET HEALTHCARE LOGS
// =====================================================

async function getLogs() {

    const result =
        await sendRequest(
            "getLogs"
        );

    if (!result.success) {

        console.error(
            result.status
        );

        return;
    }

    console.log(
        "Healthcare Logs:",
        result.appointments
    );

    displayLogs(
        result.appointments
    );
}


// =====================================================
// DISPLAY LOGS
// =====================================================

function displayLogs(records) {

    const container =
        document.getElementById(
            "logsContainer"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";


    records.forEach(record => {

        const item =
            document.createElement("div");

        item.className =
            "log-card";


        item.innerHTML = `
            <h3>
                ${escapeHTML(
                    record["Patient Name"] || ""
                )}
            </h3>

            <p>
                Doctor:
                ${escapeHTML(
                    record["Doctor Name"] || ""
                )}
            </p>

            <p>
                Appointment:
                ${escapeHTML(
                    record["Appointment Date"] || ""
                )}
                ${escapeHTML(
                    record["Appointment Time"] || ""
                )}
            </p>

            <p>
                Medication:
                ${escapeHTML(
                    record["Medication Information"] || ""
                )}
            </p>
        `;


        container.appendChild(
            item
        );

    });
}


// =====================================================
// GENERATE AI SUMMARY
// =====================================================

async function generateSummary(id) {

    if (!id) {

        alert(
            "Record ID is required."
        );

        return;
    }


    const result =
        await sendRequest(
            "generateSummary",
            {
                id: id
            }
        );


    if (result.success) {

        console.log(
            "AI Summary:",
            result.summary
        );

        return result.summary;

    } else {

        alert(
            result.status ||
            "Unable to generate summary."
        );
    }
}


// =====================================================
// GET DASHBOARD STATISTICS
// =====================================================

async function getStats() {

    const result =
        await sendRequest(
            "getStats"
        );


    if (!result.success) {
        return;
    }


    console.log(
        "Dashboard Statistics:",
        result.statistics
    );


    const total =
        document.getElementById(
            "totalRecords"
        );

    if (total) {

        total.textContent =
            result.statistics.total_records;
    }


    const pending =
        document.getElementById(
            "pendingReminders"
        );

    if (pending) {

        pending.textContent =
            result.statistics.pending_reminders;
    }


    const completed =
        document.getElementById(
            "completedReminders"
        );

    if (completed) {

        completed.textContent =
            result.statistics.completed_reminders;
    }
}


// =====================================================
// DELETE RECORD
// =====================================================

async function deleteLog(id) {

    if (!id) {
        return;
    }


    const result =
        await sendRequest(
            "deleteLog",
            {
                id: id
            }
        );


    if (result.success) {

        alert(
            "Record deleted successfully."
        );

        getLogs();

    } else {

        alert(
            result.status
        );
    }
}


// =====================================================
// HTML SAFETY
// =====================================================

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// =====================================================
// START APPLICATION
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "RK Health frontend loaded."
        );

        getLogs();
        getStats();

    }
);