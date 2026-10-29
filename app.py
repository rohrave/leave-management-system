from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Educational demo only: in-memory data is lost when the process restarts.
leave_requests = []
next_id = 1


@app.route("/")
def home():
    return render_template("index.html", leaves=leave_requests, version=app.config.get("APP_VERSION", "V1"))


@app.route("/apply", methods=["POST"])
def apply_leave():
    global next_id
    name = request.form.get("name", "").strip()
    reason = request.form.get("reason", "").strip()
    days_text = request.form.get("days", "").strip()

    if not name or not reason or not days_text:
        return "All fields are required.", 400

    try:
        days = int(days_text)
    except ValueError:
        return "Enter a valid number of leave days.", 400

    if not 1 <= days <= 365:
        return "Leave days must be between 1 and 365.", 400

    leave_requests.append({
        "id": next_id,
        "name": name,
        "reason": reason,
        "days": days,
        "status": "Pending"
    })
    next_id += 1
    return redirect(url_for("home"))


@app.route("/approve")
def approve_page():
    return render_template("approve.html", leaves=leave_requests)


@app.route("/approve/<int:leave_id>", methods=["POST"])
def approve_leave(leave_id):
    leave = next((item for item in leave_requests if item["id"] == leave_id), None)
    if leave is None:
        return "Leave request not found.", 404
    if leave["status"] != "Pending":
        return "Only pending requests can be approved.", 400
    leave["status"] = "Approved"
    return redirect(url_for("approve_page"))


@app.route("/reject/<int:leave_id>", methods=["POST"])
def reject_leave(leave_id):
    leave = next((item for item in leave_requests if item["id"] == leave_id), None)
    if leave is None:
        return "Leave request not found.", 404
    if leave["status"] != "Pending":
        return "Only pending requests can be rejected.", 400
    leave["status"] = "Rejected"
    return redirect(url_for("approve_page"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
