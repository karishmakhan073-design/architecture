<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="RK Health Patient Reminder and Health Record Management System"
    >

    <title>RK Health Dashboard</title>


    <!-- Google Fonts -->

    <link
        rel="preconnect"
        href="https://fonts.googleapis.com"
    >

    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin
    >

    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
        rel="stylesheet"
    >


    <!-- Font Awesome -->

    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
    >


    <!-- CSS -->

    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='style.css') }}"
    >

</head>


<body>


<!-- =================================================
     MOBILE OVERLAY
================================================== -->

<div
    id="sidebarOverlay"
    class="sidebar-overlay"
></div>


<!-- =================================================
     SIDEBAR
================================================== -->

<aside
    id="sidebar"
    class="sidebar"
>

    <div class="brand">

        <div class="brand-icon">

            <i class="fa-solid fa-heart-pulse"></i>

        </div>

        <div>

            <h2>RK Health</h2>

            <span>Healthcare Dashboard</span>

        </div>

    </div>


    <nav class="navigation">

        <a
            href="#dashboard"
            class="nav-link active"
        >

            <i class="fa-solid fa-house"></i>

            <span>Dashboard</span>

        </a>


        <a
            href="#add-entry"
            class="nav-link"
        >

            <i class="fa-solid fa-plus"></i>

            <span>Add Entry</span>

        </a>


        <a
            href="#logs"
            class="nav-link"
        >

            <i class="fa-solid fa-file-medical"></i>

            <span>View Logs</span>

        </a>


        <a
            href="#report"
            class="nav-link"
        >

            <i class="fa-solid fa-chart-column"></i>

            <span>Health Report</span>

        </a>

    </nav>


    <div class="sidebar-footer">

        <i class="fa-solid fa-shield-heart"></i>

        <span>
            Your health records
            at one place
        </span>

    </div>

</aside>


<!-- =================================================
     MAIN AREA
================================================== -->

<div class="main-wrapper">


    <!-- HEADER -->

    <header class="topbar">

        <div class="topbar-left">

            <button
                id="menuButton"
                class="menu-button"
                aria-label="Open navigation"
            >

                <i class="fa-solid fa-bars"></i>

            </button>


            <div>

                <h1>Health Dashboard</h1>

                <p>
                    Manage appointments,
                    medications and health records.
                </p>

            </div>

        </div>


        <div class="topbar-right">

            <div class="notification-icon">

                <i class="fa-regular fa-bell"></i>

                <span class="notification-dot"></span>

            </div>


            <div class="profile">

                <div class="profile-avatar">

                    <i class="fa-solid fa-user"></i>

                </div>

                <span>Patient</span>

            </div>

        </div>

    </header>


    <main>


        <!-- =================================================
             DASHBOARD
        ================================================== -->

        <section
            id="dashboard"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Dashboard Overview</h2>

                    <p>
                        Monitor your healthcare activities.
                    </p>

                </div>

                <button
                    class="primary-button"
                    onclick="showSection('add-entry')"
                >

                    <i class="fa-solid fa-plus"></i>

                    Add Entry

                </button>

            </div>


            <!-- STATISTICS -->

            <div class="stats-grid">


                <div class="stat-card">

                    <div class="stat-icon appointment-icon">

                        <i class="fa-solid fa-calendar-check"></i>

                    </div>

                    <div>

                        <span>
                            Appointments
                        </span>

                        <strong id="appointmentCount">
                            0
                        </strong>

                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon medicine-icon">

                        <i class="fa-solid fa-pills"></i>

                    </div>

                    <div>

                        <span>
                            Medication Reminders
                        </span>

                        <strong id="medicationCount">
                            0
                        </strong>

                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon compliance-icon">

                        <i class="fa-solid fa-chart-line"></i>

                    </div>

                    <div>

                        <span>
                            Compliance
                        </span>

                        <strong id="complianceCount">
                            0%
                        </strong>

                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon activity-icon">

                        <i class="fa-solid fa-clock-rotate-left"></i>

                    </div>

                    <div>

                        <span>
                            Recent Activity
                        </span>

                        <strong id="activityCount">
                            0
                        </strong>

                    </div>

                </div>

            </div>


            <!-- QUICK ACTIONS -->

            <div class="quick-actions">

                <button
                    class="quick-card"
                    onclick="showSection('add-entry')"
                >

                    <i class="fa-solid fa-calendar-plus"></i>

                    <div>

                        <strong>
                            Add Appointment
                        </strong>

                        <span>
                            Schedule a doctor visit
                        </span>

                    </div>

                </button>


                <button
                    class="quick-card"
                    onclick="showSection('add-entry')"
                >

                    <i class="fa-solid fa-prescription-bottle-medical"></i>

                    <div>

                        <strong>
                            Add Medication
                        </strong>

                        <span>
                            Set medicine reminder
                        </span>

                    </div>

                </button>


                <button
                    class="quick-card"
                    onclick="showSection('report')"
                >

                    <i class="fa-solid fa-file-medical"></i>

                    <div>

                        <strong>
                            Health Report
                        </strong>

                        <span>
                            View health records
                        </span>

                    </div>

                </button>

            </div>

        </section>


        <!-- =================================================
             ADD ENTRY
        ================================================== -->

        <section
            id="add-entry"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Add Healthcare Entry</h2>

                    <p>
                        Add appointment or medication information.
                    </p>

                </div>

            </div>


            <div class="forms-grid">


                <!-- APPOINTMENT FORM -->

                <div class="form-card">

                    <div class="form-title">

                        <div class="form-title-icon">

                            <i class="fa-solid fa-calendar-check"></i>

                        </div>

                        <div>

                            <h3>Appointment</h3>

                            <p>
                                Add a doctor appointment.
                            </p>

                        </div>

                    </div>


                    <form
                        id="appointmentForm"
                    >

                        <div class="form-group">

                            <label for="patientName">
                                Patient Name
                            </label>

                            <input
                                type="text"
                                id="patientName"
                                placeholder="Enter patient name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="doctorName">
                                Doctor Name
                            </label>

                            <input
                                type="text"
                                id="doctorName"
                                placeholder="Enter doctor name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="appointmentTitle">
                                Appointment Title
                            </label>

                            <input
                                type="text"
                                id="appointmentTitle"
                                placeholder="Example: General Checkup"
                                required
                            >

                        </div>


                        <div class="form-row">

                            <div class="form-group">

                                <label for="appointmentDate">
                                    Date
                                </label>

                                <input
                                    type="date"
                                    id="appointmentDate"
                                    required
                                >

                            </div>


                            <div class="form-group">

                                <label for="appointmentTime">
                                    Time
                                </label>

                                <input
                                    type="time"
                                    id="appointmentTime"
                                    required
                                >

                            </div>

                        </div>


                        <div class="form-group">

                            <label for="visitNotes">
                                Visit Notes
                            </label>

                            <textarea
                                id="visitNotes"
                                placeholder="Enter visit notes..."
                            ></textarea>

                        </div>


                        <button
                            type="submit"
                            class="primary-button full-button"
                        >

                            <i class="fa-solid fa-save"></i>

                            Save Appointment

                        </button>

                    </form>

                </div>


                <!-- MEDICATION FORM -->

                <div class="form-card">

                    <div class="form-title">

                        <div class="form-title-icon medicine-title">

                            <i class="fa-solid fa-pills"></i>

                        </div>

                        <div>

                            <h3>Medication</h3>

                            <p>
                                Create a medicine reminder.
                            </p>

                        </div>

                    </div>


                    <form
                        id="medicationForm"
                    >

                        <div class="form-group">

                            <label for="medicinePatient">
                                Patient Name
                            </label>

                            <input
                                type="text"
                                id="medicinePatient"
                                placeholder="Enter patient name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="medicineName">
                                Medicine Name
                            </label>

                            <input
                                type="text"
                                id="medicineName"
                                placeholder="Enter medicine name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="dosage">
                                Dosage
                            </label>

                            <input
                                type="text"
                                id="dosage"
                                placeholder="Example: 1 tablet"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="timing">
                                Timing
                            </label>

                            <input
                                type="text"
                                id="timing"
                                placeholder="Example: Morning"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="phoneNumber">
                                Phone Number
                            </label>

                            <input
                                type="tel"
                                id="phoneNumber"
                                placeholder="+919876543210"
                                required
                            >

                        </div>


                        <button
                            type="submit"
                            class="primary-button full-button"
                        >

                            <i class="fa-solid fa-bell"></i>

                            Save Reminder

                        </button>

                    </form>

                </div>

            </div>

        </section>


        <!-- =================================================
             LOGS
        ================================================== -->

        <section
            id="logs"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Healthcare Logs</h2>

                    <p>
                        View appointments and medication records.
                    </p>

                </div>

                <button
                    class="secondary-button"
                    onclick="loadRecords()"
                >

                    <i class="fa-solid fa-arrows-rotate"></i>

                    Refresh

                </button>

            </div>


            <div class="logs-grid">


                <!-- APPOINTMENTS -->

                <div class="log-panel">

                    <div class="panel-header">

                        <h3>

                            <i class="fa-solid fa-calendar-check"></i>

                            Appointments

                        </h3>

                    </div>


                    <div
                        id="appointmentsList"
                        class="records-container"
                    >

                        <div class="loading">
                            Loading...
                        </div>

                    </div>

                </div>


                <!-- MEDICATIONS -->

                <div class="log-panel">

                    <div class="panel-header">

                        <h3>

                            <i class="fa-solid fa-pills"></i>

                            Medications

                        </h3>

                    </div>


                    <div
                        id="medicationsList"
                        class="records-container"
                    >

                        <div class="loading">
                            Loading...
                        </div>

                    </div>

                </div>

            </div>

        </section>


        <!-- =================================================
             HEALTH REPORT
        ================================================== -->

        <section
            id="report"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Health Report</h2>

                    <p>
                        Consolidated healthcare information.
                    </p>

                </div>

                <button
                    class="primary-button"
                    onclick="printReport()"
                >

                    <i class="fa-solid fa-print"></i>

                    Print Report

                </button>

            </div>


            <div
                id="healthReport"
                class="report-card"
            >

                <div class="report-header">

                    <div>

                        <h2>
                            <i class="fa-solid fa-heart-pulse"></i>
                            RK Health Report
                        </h2>

                        <p>
                            Patient healthcare summary
                        </p>

                    </div>

                    <span id="reportDate"></span>

                </div>


                <div class="report-stat-grid">

                    <div>

                        <span>
                            Appointments
                        </span>

                        <strong id="reportAppointments">
                            0
                        </strong>

                    </div>


                    <div>

                        <span>
                            Medications
                        </span>

                        <strong id="reportMedications">
                            0
                        </strong>

                    </div>


                    <div>

                        <span>
                            Compliance
                        </span>

                        <strong id="reportCompliance">
                            0%
                        </strong>

                    </div>

                </div>


                <div class="report-section">

                    <h3>
                        Recent Appointments
                    </h3>

                    <div
                        id="reportAppointmentsList"
                    >
                    </div>

                </div>


                <div class="report-section">

                    <h3>
                        Medication Records
                    </h3>

                    <div
                        id="reportMedicationsList"
                    >
                    </div>

                </div>


                <div class="report-section">

                    <h3>
                        AI Health Summaries
                    </h3>

                    <div
                        id="reportSummaries"
                    >

                        <p class="empty-message">
                            AI summaries will appear here.
                        </p>

                    </div>

                </div>

            </div>

        </section>

    </main>

</div>


<!-- =================================================
     AI SUMMARY MODAL
================================================== -->

<div
    id="summaryModal"
    class="modal"
    role="dialog"
    aria-modal="true"
>

    <div class="modal-content">

        <div class="modal-header">

            <div>

                <h2>
                    <i class="fa-solid fa-robot"></i>

                    AI Health Summary
                </h2>

                <p>
                    Patient-friendly visit summary
                </p>

            </div>


            <button
                class="close-button"
                onclick="closeSummaryModal()"
                aria-label="Close"
            >

                <i class="fa-solid fa-xmark"></i>

            </button>

        </div>


        <div
            id="summaryContent"
            class="summary-content"
        >

            Generating summary...

        </div>


        <div class="modal-footer">

            <button
                class="secondary-button"
                onclick="closeSummaryModal()"
            >

                Close

            </button>

        </div>

    </div>

</div>


<!-- =================================================
     TOAST NOTIFICATION
================================================== -->

<div
    id="toast"
    class="toast"
>

    <i
        id="toastIcon"
        class="fa-solid fa-circle-check"
    ></i>

    <span id="toastMessage">
        Success
    </span>

</div>


<!-- JAVASCRIPT -->

<script
    src="{{ url_for('static', filename='script.js') }}"
></script>


</body>

</html><!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="RK Health Patient Reminder and Health Record Management System"
    >

    <title>RK Health Dashboard</title>


    <!-- Google Fonts -->

    <link
        rel="preconnect"
        href="https://fonts.googleapis.com"
    >

    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin
    >

    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
        rel="stylesheet"
    >


    <!-- Font Awesome -->

    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
    >


    <!-- CSS -->

    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='style.css') }}"
    >

</head>


<body>


<!-- =================================================
     MOBILE OVERLAY
================================================== -->

<div
    id="sidebarOverlay"
    class="sidebar-overlay"
></div>


<!-- =================================================
     SIDEBAR
================================================== -->

<aside
    id="sidebar"
    class="sidebar"
>

    <div class="brand">

        <div class="brand-icon">

            <i class="fa-solid fa-heart-pulse"></i>

        </div>

        <div>

            <h2>RK Health</h2>

            <span>Healthcare Dashboard</span>

        </div>

    </div>


    <nav class="navigation">

        <a
            href="#dashboard"
            class="nav-link active"
        >

            <i class="fa-solid fa-house"></i>

            <span>Dashboard</span>

        </a>


        <a
            href="#add-entry"
            class="nav-link"
        >

            <i class="fa-solid fa-plus"></i>

            <span>Add Entry</span>

        </a>


        <a
            href="#logs"
            class="nav-link"
        >

            <i class="fa-solid fa-file-medical"></i>

            <span>View Logs</span>

        </a>


        <a
            href="#report"
            class="nav-link"
        >

            <i class="fa-solid fa-chart-column"></i>

            <span>Health Report</span>

        </a>

    </nav>


    <div class="sidebar-footer">

        <i class="fa-solid fa-shield-heart"></i>

        <span>
            Your health records
            at one place
        </span>

    </div>

</aside>


<!-- =================================================
     MAIN AREA
================================================== -->

<div class="main-wrapper">


    <!-- HEADER -->

    <header class="topbar">

        <div class="topbar-left">

            <button
                id="menuButton"
                class="menu-button"
                aria-label="Open navigation"
            >

                <i class="fa-solid fa-bars"></i>

            </button>


            <div>

                <h1>Health Dashboard</h1>

                <p>
                    Manage appointments,
                    medications and health records.
                </p>

            </div>

        </div>


        <div class="topbar-right">

            <div class="notification-icon">

                <i class="fa-regular fa-bell"></i>

                <span class="notification-dot"></span>

            </div>


            <div class="profile">

                <div class="profile-avatar">

                    <i class="fa-solid fa-user"></i>

                </div>

                <span>Patient</span>

            </div>

        </div>

    </header>


    <main>


        <!-- =================================================
             DASHBOARD
        ================================================== -->

        <section
            id="dashboard"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Dashboard Overview</h2>

                    <p>
                        Monitor your healthcare activities.
                    </p>

                </div>

                <button
                    class="primary-button"
                    onclick="showSection('add-entry')"
                >

                    <i class="fa-solid fa-plus"></i>

                    Add Entry

                </button>

            </div>


            <!-- STATISTICS -->

            <div class="stats-grid">


                <div class="stat-card">

                    <div class="stat-icon appointment-icon">

                        <i class="fa-solid fa-calendar-check"></i>

                    </div>

                    <div>

                        <span>
                            Appointments
                        </span>

                        <strong id="appointmentCount">
                            0
                        </strong>

                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon medicine-icon">

                        <i class="fa-solid fa-pills"></i>

                    </div>

                    <div>

                        <span>
                            Medication Reminders
                        </span>

                        <strong id="medicationCount">
                            0
                        </strong>

                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon compliance-icon">

                        <i class="fa-solid fa-chart-line"></i>

                    </div>

                    <div>

                        <span>
                            Compliance
                        </span>

                        <strong id="complianceCount">
                            0%
                        </strong>

                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon activity-icon">

                        <i class="fa-solid fa-clock-rotate-left"></i>

                    </div>

                    <div>

                        <span>
                            Recent Activity
                        </span>

                        <strong id="activityCount">
                            0
                        </strong>

                    </div>

                </div>

            </div>


            <!-- QUICK ACTIONS -->

            <div class="quick-actions">

                <button
                    class="quick-card"
                    onclick="showSection('add-entry')"
                >

                    <i class="fa-solid fa-calendar-plus"></i>

                    <div>

                        <strong>
                            Add Appointment
                        </strong>

                        <span>
                            Schedule a doctor visit
                        </span>

                    </div>

                </button>


                <button
                    class="quick-card"
                    onclick="showSection('add-entry')"
                >

                    <i class="fa-solid fa-prescription-bottle-medical"></i>

                    <div>

                        <strong>
                            Add Medication
                        </strong>

                        <span>
                            Set medicine reminder
                        </span>

                    </div>

                </button>


                <button
                    class="quick-card"
                    onclick="showSection('report')"
                >

                    <i class="fa-solid fa-file-medical"></i>

                    <div>

                        <strong>
                            Health Report
                        </strong>

                        <span>
                            View health records
                        </span>

                    </div>

                </button>

            </div>

        </section>


        <!-- =================================================
             ADD ENTRY
        ================================================== -->

        <section
            id="add-entry"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Add Healthcare Entry</h2>

                    <p>
                        Add appointment or medication information.
                    </p>

                </div>

            </div>


            <div class="forms-grid">


                <!-- APPOINTMENT FORM -->

                <div class="form-card">

                    <div class="form-title">

                        <div class="form-title-icon">

                            <i class="fa-solid fa-calendar-check"></i>

                        </div>

                        <div>

                            <h3>Appointment</h3>

                            <p>
                                Add a doctor appointment.
                            </p>

                        </div>

                    </div>


                    <form
                        id="appointmentForm"
                    >

                        <div class="form-group">

                            <label for="patientName">
                                Patient Name
                            </label>

                            <input
                                type="text"
                                id="patientName"
                                placeholder="Enter patient name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="doctorName">
                                Doctor Name
                            </label>

                            <input
                                type="text"
                                id="doctorName"
                                placeholder="Enter doctor name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="appointmentTitle">
                                Appointment Title
                            </label>

                            <input
                                type="text"
                                id="appointmentTitle"
                                placeholder="Example: General Checkup"
                                required
                            >

                        </div>


                        <div class="form-row">

                            <div class="form-group">

                                <label for="appointmentDate">
                                    Date
                                </label>

                                <input
                                    type="date"
                                    id="appointmentDate"
                                    required
                                >

                            </div>


                            <div class="form-group">

                                <label for="appointmentTime">
                                    Time
                                </label>

                                <input
                                    type="time"
                                    id="appointmentTime"
                                    required
                                >

                            </div>

                        </div>


                        <div class="form-group">

                            <label for="visitNotes">
                                Visit Notes
                            </label>

                            <textarea
                                id="visitNotes"
                                placeholder="Enter visit notes..."
                            ></textarea>

                        </div>


                        <button
                            type="submit"
                            class="primary-button full-button"
                        >

                            <i class="fa-solid fa-save"></i>

                            Save Appointment

                        </button>

                    </form>

                </div>


                <!-- MEDICATION FORM -->

                <div class="form-card">

                    <div class="form-title">

                        <div class="form-title-icon medicine-title">

                            <i class="fa-solid fa-pills"></i>

                        </div>

                        <div>

                            <h3>Medication</h3>

                            <p>
                                Create a medicine reminder.
                            </p>

                        </div>

                    </div>


                    <form
                        id="medicationForm"
                    >

                        <div class="form-group">

                            <label for="medicinePatient">
                                Patient Name
                            </label>

                            <input
                                type="text"
                                id="medicinePatient"
                                placeholder="Enter patient name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="medicineName">
                                Medicine Name
                            </label>

                            <input
                                type="text"
                                id="medicineName"
                                placeholder="Enter medicine name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="dosage">
                                Dosage
                            </label>

                            <input
                                type="text"
                                id="dosage"
                                placeholder="Example: 1 tablet"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="timing">
                                Timing
                            </label>

                            <input
                                type="text"
                                id="timing"
                                placeholder="Example: Morning"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="phoneNumber">
                                Phone Number
                            </label>

                            <input
                                type="tel"
                                id="phoneNumber"
                                placeholder="+919876543210"
                                required
                            >

                        </div>


                        <button
                            type="submit"
                            class="primary-button full-button"
                        >

                            <i class="fa-solid fa-bell"></i>

                            Save Reminder

                        </button>

                    </form>

                </div>

            </div>

        </section>


        <!-- =================================================
             LOGS
        ================================================== -->

        <section
            id="logs"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Healthcare Logs</h2>

                    <p>
                        View appointments and medication records.
                    </p>

                </div>

                <button
                    class="secondary-button"
                    onclick="loadRecords()"
                >

                    <i class="fa-solid fa-arrows-rotate"></i>

                    Refresh

                </button>

            </div>


            <div class="logs-grid">


                <!-- APPOINTMENTS -->

                <div class="log-panel">

                    <div class="panel-header">

                        <h3>

                            <i class="fa-solid fa-calendar-check"></i>

                            Appointments

                        </h3>

                    </div>


                    <div
                        id="appointmentsList"
                        class="records-container"
                    >

                        <div class="loading">
                            Loading...
                        </div>

                    </div>

                </div>


                <!-- MEDICATIONS -->

                <div class="log-panel">

                    <div class="panel-header">

                        <h3>

                            <i class="fa-solid fa-pills"></i>

                            Medications

                        </h3>

                    </div>


                    <div
                        id="medicationsList"
                        class="records-container"
                    >

                        <div class="loading">
                            Loading...
                        </div>

                    </div>

                </div>

            </div>

        </section>


        <!-- =================================================
             HEALTH REPORT
        ================================================== -->

        <section
            id="report"
            class="page-section"
        >

            <div class="section-heading">

                <div>

                    <h2>Health Report</h2>

                    <p>
                        Consolidated healthcare information.
                    </p>

                </div>

                <button
                    class="primary-button"
                    onclick="printReport()"
                >

                    <i class="fa-solid fa-print"></i>

                    Print Report

                </button>

            </div>


            <div
                id="healthReport"
                class="report-card"
            >

                <div class="report-header">

                    <div>

                        <h2>
                            <i class="fa-solid fa-heart-pulse"></i>
                            RK Health Report
                        </h2>

                        <p>
                            Patient healthcare summary
                        </p>

                    </div>

                    <span id="reportDate"></span>

                </div>


                <div class="report-stat-grid">

                    <div>

                        <span>
                            Appointments
                        </span>

                        <strong id="reportAppointments">
                            0
                        </strong>

                    </div>


                    <div>

                        <span>
                            Medications
                        </span>

                        <strong id="reportMedications">
                            0
                        </strong>

                    </div>


                    <div>

                        <span>
                            Compliance
                        </span>

                        <strong id="reportCompliance">
                            0%
                        </strong>

                    </div>

                </div>


                <div class="report-section">

                    <h3>
                        Recent Appointments
                    </h3>

                    <div
                        id="reportAppointmentsList"
                    >
                    </div>

                </div>


                <div class="report-section">

                    <h3>
                        Medication Records
                    </h3>

                    <div
                        id="reportMedicationsList"
                    >
                    </div>

                </div>


                <div class="report-section">

                    <h3>
                        AI Health Summaries
                    </h3>

                    <div
                        id="reportSummaries"
                    >

                        <p class="empty-message">
                            AI summaries will appear here.
                        </p>

                    </div>

                </div>

            </div>

        </section>

    </main>

</div>


<!-- =================================================
     AI SUMMARY MODAL
================================================== -->

<div
    id="summaryModal"
    class="modal"
    role="dialog"
    aria-modal="true"
>

    <div class="modal-content">

        <div class="modal-header">

            <div>

                <h2>
                    <i class="fa-solid fa-robot"></i>

                    AI Health Summary
                </h2>

                <p>
                    Patient-friendly visit summary
                </p>

            </div>


            <button
                class="close-button"
                onclick="closeSummaryModal()"
                aria-label="Close"
            >

                <i class="fa-solid fa-xmark"></i>

            </button>

        </div>


        <div
            id="summaryContent"
            class="summary-content"
        >

            Generating summary...

        </div>


        <div class="modal-footer">

            <button
                class="secondary-button"
                onclick="closeSummaryModal()"
            >

                Close

            </button>

        </div>

    </div>

</div>


<!-- =================================================
     TOAST NOTIFICATION
================================================== -->

<div
    id="toast"
    class="toast"
>

    <i
        id="toastIcon"
        class="fa-solid fa-circle-check"
    ></i>

    <span id="toastMessage">
        Success
    </span>

</div>


<!-- JAVASCRIPT -->

<script
    src="{{ url_for('static', filename='script.js') }}"
></script>


</body>

</html>