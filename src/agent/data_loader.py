"""
Data Loader - Efficient Parquet access via DuckDB (Christian)
"""
import duckdb
from pathlib import Path
from typing import List, Optional
import pandas as pd


class DataLoader:
    """
    Loads data from Parquet files using DuckDB for efficient querying.
    """

    def __init__(self, data_dir: str = "disaster_ai_sp26/datasets"):
        self.data_dir = Path(data_dir)
        self.conn = duckdb.connect()  # In-memory connection
        
    def list_datasets(self) -> List[str]:
        """Return list of available parquet files."""
        return [f.name for f in self.data_dir.glob("*.parquet")]

    def get_columns(self, filename: str) -> List[str]:
        """Get column names from a parquet file."""
        filepath = self.data_dir / filename
        result = self.conn.execute(f"""
            SELECT column_name 
            FROM parquet_schema('{filepath}')
        """).fetchall()
        return [row[0] for row in result]

    def query(self, sql: str) -> pd.DataFrame:
        """Execute raw SQL against the data directory."""
        return self.conn.execute(sql).df()

    def get_feature_data(self, 
                         source_file: str, 
                         feature_column: str,
                         hex_ids: Optional[List[str]] = None,
                         limit: int = 1000) -> pd.DataFrame:
        """
        Get feature data, optionally filtered by hex IDs.
        
        Args:
            source_file: Parquet filename
            feature_column: Column to retrieve
            hex_ids: Optional list of hex IDs to filter
            limit: Max rows to return
        """
        filepath = self.data_dir / source_file
        
        if hex_ids:
            hex_list = ", ".join([f"'{h}'" for h in hex_ids])
            sql = f"""
                SELECT hex_id, {feature_column}
                FROM '{filepath}'
                WHERE hex_id IN ({hex_list})
                LIMIT {limit}
            """
        else:
            sql = f"""
                SELECT hex_id, {feature_column}
                FROM '{filepath}'
                LIMIT {limit}
            """
        
        return self.conn.execute(sql).df()

    def aggregate_feature(self, 
                          source_file: str,
                          feature_column: str,
                          aggregation: str = "SUM",
                          hex_ids: Optional[List[str]] = None) -> float:
        """
        Aggregate a feature using the specified rule.
        
        Args:
            source_file: Parquet filename
            feature_column: Column to aggregate
            aggregation: SUM, AVG, COUNT, etc.
            hex_ids: Optional hex ID filter
        """
        filepath = self.data_dir / source_file
        
        where_clause = ""
        if hex_ids:
            hex_list = ", ".join([f"'{h}'" for h in hex_ids])
            where_clause = f"WHERE hex_id IN ({hex_list})"
        
        sql = f"""
            SELECT {aggregation}({feature_column}) as result
            FROM '{filepath}'
            {where_clause}
        """
        
        result = self.conn.execute(sql).fetchone()
        return result[0] if result else None


if __name__ == "__main__":
    loader = DataLoader()
    
    print("Available datasets:")
    for ds in loader.list_datasets()[:5]:
        print(f"  - {ds}")
    
    print("\nColumns in CRIT_LIFE_001.parquet:")
    cols = loader.get_columns("CRIT_LIFE_001.parquet")
    print(f"  {cols}")
