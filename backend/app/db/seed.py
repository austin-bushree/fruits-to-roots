import json
import sqlite3


def dci_table_from_JSON(json_file, db_path="ngss.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(json_file, "r") as f:
        data = json.load(f)

    for pe_id, pe_data in data.items():
        domain = pe_data.get("domain") or "Unknown"
        topic = pe_data.get("topic") or "Unknown"
        dcis = pe_data.get("dcis", {})

        for group_code_name, ideas in dcis.items():
            parts = group_code_name.split(": ", 1)
            if len(parts) != 2:
                continue
            group_code, group_name = parts #TODO, groupname = code AND name..

            for full_idea in ideas:
                if not full_idea.strip():
                    continue
                heading = " ".join(full_idea.strip().split()[:3])
                try:
                    cursor.execute("""
                        INSERT INTO dcis (domain, topic, group_code, group_name, heading, full_idea)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ON CONFLICT(full_idea) DO NOTHING
                    """, (domain, topic, group_code, group_code_name, heading, full_idea))
                except Exception as e:
                    print(f"⚠️ Error inserting DCI: {full_idea}\n{e}")
                try:
                    #Retrieve the ID of the just inserted or existing DCI
                    cursor.execute("SELECT id FROM dcis WHERE full_idea = ?", (full_idea,))
                    dci_id = cursor.fetchone()[0]

                    #Link to the PE
                    cursor.execute("""
                    INSERT OR IGNORE INTO expectations_dcis (expectation_id, dci_id)
                    VALUES (?, ?)
                    """, (pe_id, dci_id))
                except Exception as e:
                    print(f"⚠️ Error joining DCI to a pe_id: {full_idea}\n{e}")


    conn.commit()
    conn.close()
    print("✅ DCI table seeded successfully.")


if __name__ == '__main__':
    dci_table_from_JSON("ngss.json")

# with open("ngss.json") as f:
#     data = json.load(f)
#
# conn = sqlite3.connect("app/db/ngss.db")
# cursor = conn.cursor()
#
# for key, value in data.items():
#     cursor.execute("""
#         INSERT INTO standards (id, grade_level, domain, area_code, title, description)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         key,
#         key.split("-")[0],          # e.g., 'HS'
#         key.split("-")[1][:2],      # e.g., 'PS'
#         "-".join(key.split("-")[1:2]),  # e.g., 'PS3'
#         value.get("title", ""),
#         value.get("description", "")
#     ))
#
# conn.commit()
# conn.close()