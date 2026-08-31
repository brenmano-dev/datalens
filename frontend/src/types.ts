export interface DatasetOverview {
  rows: number;
  columns: number;
}

export interface ColumnSchema {
  name: string;
  type: string;
  missing_count: number;
  missing_percentage: number;
  unique_count: number;
}

export interface Quality {
  score: number;
  duplicates: number;
  missing_values: Record<string, number>;
  outliers: Record<string, number>;
}

export interface DatasetResponse {
  dataset: DatasetOverview;
  schema: ColumnSchema[];
  quality: Quality;
  statistics: Record<string, any>;
  correlations: Record<string, number>;
  insights: string[];
  preview: any[];
}
