interface ResultTableProps {
  rows: Record<string, unknown>[];
  columns: string[];
}

export function ResultTable({
  rows,
  columns,
}: ResultTableProps) {
  return (
    <section className="panel">
      <div className="panel-title">
        Results
      </div>

      {rows.length === 0 ? (
        <div className="empty-state">
          No rows returned.
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column}>
                    {column}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {columns.map((column) => (
                    <td key={`${rowIndex}-${column}`}>
                      {formatValue(row[column])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function formatValue(
  value: unknown,
): string {
  if (value === null || value === undefined) {
    return "NULL";
  }

  if (
    typeof value === "object"
  ) {
    return JSON.stringify(value);
  }

  return String(value);
}
