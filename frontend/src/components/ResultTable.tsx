interface ResultTableProps {
  rows: Record<string, unknown>[];
  columns: string[];
}

export function ResultTable({ rows, columns }: ResultTableProps) {
  return (
    <section className="results-card">
      <div className="results-header">
        <h2 className="results-title">Query Results</h2>
        <span className="results-count">
          {rows.length} {rows.length === 1 ? "row" : "rows"}
        </span>
      </div>

      {rows.length === 0 ? (
        <div className="empty-results">
          No records returned. Execute a query to display database records.
        </div>
      ) : (
        <div className="table-wrapper">
          <table className="editorial-table">
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column}>{column}</th>
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

function formatValue(value: unknown): React.ReactNode {
  if (value === null || value === undefined) {
    return <span className="null-pill">NULL</span>;
  }

  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}
