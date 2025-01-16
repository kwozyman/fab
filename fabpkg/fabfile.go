package fabpkg

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

type FabfileMetadata struct {
	Name        string `yaml:"name"`
	Description string `yaml:"description"`
}

type FabFile struct {
	Metadata       FabfileMetadata `yaml:"metadata"`
	From           string          `yaml:"from"`
	IncludeFiles   []string        `yaml:"include"`
	IncludeModules []FabModule
	BuildArgs      []map[string]string `yaml:"buildargs"`
}

func ParseFabFileYAML(filePath string) (*FabFile, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not open file: %w", err)
	}
	defer file.Close()

	var fabfile FabFile
	yamlDecoder := yaml.NewDecoder(file)
	if err := yamlDecoder.Decode(&fabfile); err != nil {
		return nil, fmt.Errorf("could not decode YAML: %w", err)
	}

	for _, element := range fabfile.IncludeFiles {
		fabModule, err := ParseModuleYAML(element)
		if err != nil {
			return nil, fmt.Errorf("could not load included module: %w", err)
		}
		fabfile.IncludeModules = append(fabfile.IncludeModules, *fabModule)
	}

	return &fabfile, nil
}
