package fabpkg

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

type ModuleMetadata struct {
	Name        string `yaml:"name"`
	Description string `yaml:"description"`
}

type FabModule struct {
	Metadata      ModuleMetadata `yaml:"metadata"`
	Containerfile string         `yaml:"containerfile"`
	BuildArgs     []string       `yaml:"buildargs"`
	BaseDir       string         ``
}

func (fabmodule FabModule) GetFullContainerfilePath() string {
	return filepath.Join(fabmodule.BaseDir, fabmodule.Containerfile)
}

func ParseModuleYAML(filePath string) (*FabModule, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not open file %w", err)
	}
	defer file.Close()

	var module FabModule
	yamlDecoder := yaml.NewDecoder(file)
	if err := yamlDecoder.Decode(&module); err != nil {
		return nil, fmt.Errorf("error decoding YAML: %w", err)
	}

	absoluteFilePath, err := filepath.Abs(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not get absolute path: %w", err)
	}
	module.BaseDir = filepath.Dir(absoluteFilePath)

	return &module, nil
}
