from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

JSONValue = Any

class CreatePipelineRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    target_namespace: str
    distance_metric: str | None = "cosine_distance"

class Pipeline(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    target_namespace: str
    distance_metric: str
    created_at: str

class PipelineList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pipelines: list[Pipeline]

class PipelineStatus(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pipeline_id: str
    counts: dict[str, int]
    pending_count: int
    processing_count: int
    failed_count: int
    indexed_rate_per_min: float
    rate_window_seconds: int

class ClaimDocumentsRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    stage: str | None = "pending"
    claim_stage: str | None = "embedding"
    limit: int | None = 100
    worker_id: str
    lease_seconds: int | None = 900
    document_id_prefix: str | None = None

class ClaimDocumentsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pipeline_id: str
    stage: str
    claim_stage: str
    worker_id: str
    documents: list[str]

class HeartbeatDocumentsRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    document_ids: list[str]
    stage: str | None = "embedding"
    worker_id: str

class SetDocumentsStageRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    document_ids: list[str]
    stage: str
    from_stage: str | None = None
    worker_id: str | None = None
    create_missing: bool | None = False

class DocumentsStageResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pipeline_id: str
    stage: str
    updated: int

class StageDocumentResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pipeline_id: str
    document_id: str
    stage: str
    chunk_count: int
    chunk_ids: list[str]

class Chunk(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    text: str | None = None
    metadata: dict[str, Any] | None = None

class PutChunksRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    chunks: list[Chunk]

GetChunksResponse = list[Chunk]

class VectorEntry(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    vector: list[float]
    attributes: dict[str, Any] | None = None

class PutVectorsRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    vectors: list[VectorEntry]

class CreateUdfRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    spec: UdfSpec

class Udf(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    spec: UdfSpec
    paused: bool
    created_at: str
    updated_at: str

class UdfList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    udfs: list[Udf]

class GetUdfResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    udf: Udf
    status: UdfStatus

class UdfStatus(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    udf_id: str
    paused: bool
    active_namespaces: list[str]
    discovery: UdfDiscoveryStatus
    counts: dict[str, int]
    pending_count: int
    processing_count: int
    failed_count: int
    indexed_rate_per_min: float
    rate_window_seconds: int

class UdfDiscoveryStatus(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    sweeps_completed: int
    last_completed_at: str | None

class UdfSpec(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    index_selector: Any | None = None
    target_namespaces: list[str] | None = []
    inputs: list[str] | None = []
    version: str | None = "v1"
    filter: Any | None = None
    worker: UdfWorkerSpec
    schedule: UdfScheduleSpec | None = None
    retry: UdfRetrySpec | None = None
    triggers: list[UdfTrigger] | None = ["discovery"]
    invalidates: list[str] | None = []

UdfTrigger = Literal["discovery", "write"]

class UdfWorkerSpec(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    image: str | None = None
    url: str | None = None
    port: int | None = None
    batch_size: int | None = 32
    timeout_seconds: int | None = 30
    pod_spec: Any | None = None

class UdfScheduleSpec(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    discovery_interval_seconds: int | None = 60
    lease_seconds: int | None = 120
    max_in_flight_batches: int | None = 8
    max_concurrent_scans: int | None = 4

class UdfRetrySpec(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    max_attempts: int | None = 8
    initial_backoff_seconds: int | None = 5
    max_backoff_seconds: int | None = 300

class UdfDiscoverRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespaces: list[str] | None = []
    page_size: int | None = 10000

class UdfDiscoverResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    udf_id: str
    enqueued: int
    namespaces: list[str]

class UdfClaimRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    worker_id: str
    limit: int | None = 32
    lease_seconds: int | None = 120

class UdfClaimedItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespace: str
    id: str
    input: dict[str, Any]

class UdfClaimResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    udf_id: str
    worker_id: str
    items: list[UdfClaimedItem]

class UdfItemRef(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespace: str
    id: str

class UdfHeartbeatRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    worker_id: str
    items: list[UdfItemRef]

class UdfCompleteRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    worker_id: str
    items: list[UdfCompleteItem]

class UdfCompleteItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespace: str
    id: str
    attributes: dict[str, Any] | None = {}

UdfErrorKind = Literal["transient", "permanent"]

class UdfFailRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    worker_id: str
    items: list[UdfFailItem]

class UdfFailItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespace: str
    id: str
    kind: UdfErrorKind
    message: str | None = None

class UdfItemsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    udf_id: str
    updated: int

class Document(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    attributes: dict[str, Any]

class FetchDocumentsRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    ids: list[str]
    include_attributes: list[str] | None = None

class FetchDocumentsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    documents: list[Document]
    missing: list[str]

class StatusResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: str
    message: str | None = None
    rows_affected: int | None = None
    rows_upserted: int | None = None
    rows_patched: int | None = None
    rows_deleted: int | None = None
    billing: dict[str, Any] | None = None

class TurbopufferNamespaceSummary(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str

class TurbopufferNamespaceList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespaces: list[TurbopufferNamespaceSummary]
    next_cursor: str | None = None

class TurbopufferSchema(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pass

class TurbopufferMetadataPatch(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pinning: Any | None = None

class TurbopufferWriteRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pass

class TurbopufferBranchFromRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    branch_from_namespace: dict[str, Any]

class TurbopufferCopyFromRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    copy_from_namespace: str | dict[str, Any]

class TurbopufferWriteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: str
    message: str
    rows_affected: int
    rows_upserted: int | None = None
    rows_patched: int | None = None
    rows_deleted: int | None = None
    rows_remaining: bool | None = None
    upserted_ids: list[Any] | None = None
    patched_ids: list[Any] | None = None
    deleted_ids: list[Any] | None = None
    billing: dict[str, Any]
    performance: dict[str, Any] | None = None

class TurbopufferQueryRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pass

class TurbopufferQueryResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    rows: list[dict[str, Any]] | None = None
    aggregations: dict[str, Any] | None = None
    aggregation_groups: list[dict[str, Any]] | None = None
    billing: dict[str, Any] | None = None
    performance: dict[str, Any] | None = None

class TurbopufferMultiQueryRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    queries: list[TurbopufferQueryRequest]
    consistency: dict[str, Any] | None = None
    vector_encoding: str | None = None

class TurbopufferMultiQueryResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    results: list[TurbopufferQueryResponse]
    billing: dict[str, Any] | None = None
    performance: dict[str, Any] | None = None
    stable_as_of: int | None = None

class TurbopufferExplainQueryResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    plan_text: str | None = None

class TurbopufferRecallRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    num: int | None = None
    top_k: int | None = None
    filters: Any | None = None
    rank_by: Any | None = None
    include_ground_truth: bool | None = None

class TurbopufferRecallResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    avg_recall: float
    avg_exhaustive_count: float
    avg_ann_count: float
    ground_truth: list[dict[str, Any]] | None = None

class HintCacheWarmResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: str | None = None
    message: str | None = None

JobStatus = Literal["running", "completed", "failed"]

SnapshotSource = Literal["auto", "stored", "cache", "origin"]

ScanSource = Literal["auto", "cache", "origin"]

ScanCountSource = Literal["auto", "snapshot", "cache", "origin"]

ScanMode = Literal["ids", "count"]

ScanCountServedBy = Literal["snapshot", "cache", "origin"]

class CreateSnapshotRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    field: str
    source: SnapshotSource | None = None
    filters: Any | None = None
    page_size: int | None = 1000

class CreateScanRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    source: ScanCountSource | None = None
    filters: Any | None = None
    fts: FtsScan | None = None
    ann: AnnScan | None = None
    mode: ScanMode | None = None
    exhaustive: bool | None = False
    threads: int | None = None
    page_size: int | None = 1000
    timeout_seconds: int | None = 30

class FtsScan(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    field: str
    query: str

class AnnScan(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    vector: list[float]
    field: str | None = "vector"
    radius: float

WarmStepStatus = Literal["skipped", "completed", "started", "no_snapshot"]

class WarmStepResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: bool
    status: WarmStepStatus

class WarmDocumentsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: bool
    status: WarmStepStatus
    job: WarmJob | None = None

class WarmSnapshotsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: bool
    status: WarmStepStatus
    key: str | None = None
    watermark_ms: int | None = None
    sha: str | None = None

class WarmCacheResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespace: str
    turbopuffer: WarmStepResponse
    documents: WarmDocumentsResponse
    snapshots: WarmSnapshotsResponse

class JobBase(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    namespace: str
    status: JobStatus
    progress: float
    documents_scanned: int
    stable_as_of: int | None = None
    created_at: str
    completed_at: str | None = None
    error: str | None = None

class SnapshotJob(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    namespace: str
    status: JobStatus
    progress: float
    documents_scanned: int
    stable_as_of: int | None = None
    created_at: str
    completed_at: str | None = None
    error: str | None = None
    field: str
    source: SnapshotSource
    effective_source: SnapshotSource | None = None
    sha: str | None = None

class SnapshotJobList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    snapshot_jobs: list[SnapshotJob]

class WarmJob(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    namespace: str
    status: JobStatus
    progress: float
    documents_scanned: int
    stable_as_of: int | None = None
    created_at: str
    completed_at: str | None = None
    error: str | None = None

class WarmJobList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    warm_jobs: list[WarmJob]

class ScanJob(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    namespace: str
    status: JobStatus
    progress: float
    documents_scanned: int
    stable_as_of: int | None = None
    created_at: str
    completed_at: str | None = None
    error: str | None = None
    source: ScanSource
    effective_source: ScanSource | None = None
    threads: int | None = None

class ScanJobList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    scans: list[ScanJob]

class FieldValueResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    value: str
    doc_count: int

class ScanIdsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    ids: list[str]
    total: int

class ScanCountResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    count: int
    served_by: ScanCountServedBy
    snapshot_sha: str | None = None
    watermark_ms: int | None = None
    bounded: bool | None = None
    timed_out: bool | None = None
    shards_saturated: int | None = None
    shards_total: int | None = None
    approximate: bool | None = None
    threads: int | None = None
    elapsed_ms: int

class NamespaceList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespaces: list[NamespaceListEntry]
    next_cursor: str | None = None

class NamespaceListEntry(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    name: str
    row_count: int | None = None
    size_bytes: int | None = None
    stable_as_of_ms: int | None = None
    is_stable: bool | None = None
    schema_summary: NamespaceSchemaSummary | None = None
    index: IndexState | None = None
    cache_state: NamespaceCacheState | None = None
    last_write_ms: int | None = None
    shadow: bool | None = None
    labels: dict[str, str] | None = None
    metadata_error: str | None = None

class NamespaceSchemaSummary(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    vector_dim: int | None = None
    fields: list[str] | None = None

class IndexState(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: Literal["updating", "up-to-date"] | None = None
    unindexed_bytes: int | None = None

class NamespaceCacheState(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    state: Literal["cold", "warming", "warm"]
    warmed_through_ms: int | None = None
    warm_inflight: bool

class NamespaceMetadata(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    schema: dict[str, Any]
    approx_logical_bytes: int
    approx_row_count: int
    created_at: str
    last_write_at: str | None = None
    updated_at: str
    config: dict[str, Any] | None = None

class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    vector: list[float] | None = None
    nearest_to_id: list[str] | None = None
    top_k: int | None = 10
    filters: Any | None = None
    include_attributes: bool | list[str] | None = None
    cursor: str | None = None

class QueryResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    rows: list[dict[str, Any]]
    aggregations: dict[str, Any] | None = None
    aggregation_groups: list[dict[str, Any]] | None = None
    billing: dict[str, Any] | None = None
    performance: dict[str, Any] | None = None
    stable_as_of: int | None = None
    next_cursor: str | None = None

class Error(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    error: str
    message: str

class SnapshotHistoryEntry(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    watermark_ms: int
    sha: str

class SnapshotBody(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    namespace: str
    watermark_ms: int
    sha: str
    fields: list[SnapshotField]
    fields_skipped: list[SnapshotFieldSkipped]

class SnapshotField(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    name: str
    values: list[SnapshotValueCount]

SnapshotSkipReason = Literal["exceeded_cap"]

class SnapshotFieldSkipped(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    name: str
    reason: SnapshotSkipReason
    distinct_observed: int
    cap: int

class SnapshotValueCount(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    v: str
    n: int

class SnapshotActivityEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    ts_ms: int
    namespace: str
    sha: str

class SnapshotActivityList(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    events: list[SnapshotActivityEvent]
    next_cursor: str | None = None
    truncated: bool | None = None

MetricKind = Literal["counter", "gauge", "histogram"]

MetricFamily = Literal["query", "upsert", "fetch", "cache", "pipeline", "storage", "saturation"]

class MetricAlert(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    summary: str
    expr: str
    for_: str = Field(..., alias="for")

class MetricCatalogEntry(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    name: str
    kind: MetricKind
    family: MetricFamily
    labels: list[str]
    description: str
    example_promql: str
    alert: MetricAlert | None = None

class MetricCatalog(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    version: str
    entries: list[MetricCatalogEntry]

class PrometheusResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    pass

class SearchHistoryEntry(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    timestamp: str
    timestamp_nanos: int
    namespace: str
    trace_id: str | None = None
    raw_query: str | None = None
    stable_as_of: int | None = None
    query: dict[str, Any]
    top_result_ids: list[str]
    tags: list[str]

class SearchHistoryListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    entries: list[SearchHistoryEntry]
    next_cursor: str | None = None

class ClickstreamEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    timestamp: str
    timestamp_nanos: int
    trace_id: str
    namespace: str
    doc_id: str
    tags: list[str]
    source: str
    served_from: str

class ClickstreamListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    events: list[ClickstreamEvent]
    next_cursor: str | None = None
