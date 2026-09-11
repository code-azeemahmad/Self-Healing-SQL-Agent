interface SqlViewerProps {
  sql: string | null;
  title?: string;
}

export function SqlViewer({
  sql,
  title = "SQL",
}: SqlViewerProps) {
  return (
    <section className="panel">
      <div className="panel-title">
        {title}
      </div>

      {sql ? (
        <pre className="sql-viewer">
          <code>{sql}</code>
        </pre>
      ) : (
        <div className="empty-state">
          SQL will appear here after generation.
        </div>
      )}
    </section>
  );
}
