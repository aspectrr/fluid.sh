package telemetry

import (
	"runtime"

	"virsh-sandbox/internal/config"

	"github.com/google/uuid"
	"github.com/posthog/posthog-go"
)

// Service defines the interface for telemetry operations.
type Service interface {
	Track(event string, properties map[string]interface{})
	Close()
}

type noopService struct{}

func (s *noopService) Track(event string, properties map[string]interface{}) {}
func (s *noopService) Close()                                                {}

type posthogService struct {
	client     posthog.Client
	distinctID string
}

// NewService creates a new telemetry service based on configuration.
func NewService(cfg config.TelemetryConfig) (Service, error) {
	if !cfg.EnableAnonymousUsage || cfg.APIKey == "" {
		return &noopService{}, nil
	}

	client, err := posthog.NewWithConfig(cfg.APIKey, posthog.Config{
		Endpoint: cfg.Endpoint,
	})
	if err != nil {
		return nil, err
	}

	// Generate a unique ID for this session.
	// In a real application, you might want to persist this ID.
	distinctID := uuid.New().String()

	return &posthogService{
		client:     client,
		distinctID: distinctID,
	}, nil
}

func (s *posthogService) Track(event string, properties map[string]interface{}) {
	if properties == nil {
		properties = make(map[string]interface{})
	}

	// Add common properties
	properties["os"] = runtime.GOOS
	properties["arch"] = runtime.GOARCH
	properties["go_version"] = runtime.Version()

	_ = s.client.Enqueue(posthog.Capture{
		DistinctId: s.distinctID,
		Event:      event,
		Properties: properties,
	})
}

func (s *posthogService) Close() {
	_ = s.client.Close()
}
