# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'peak/app_info'

Gem::Specification.new do |spec|
    spec.name = 'peak'
    spec.version = Peak::VERSION
    spec.licenses = ['Apache-2.0']
    spec.authors = ['Jeffrey Phillips Freeman']
    spec.email = ['jeffrey.freeman@syncleus.com']

    spec.summary = %q{Reference implementation for the APEX Radio protocol, an extension to APRS.}
    spec.description = %q{Reference implementation for the APEX Radio protocol, which is iteself an extension to the APRS protocol.}
    spec.homepage = 'http://apexprotocol.com'

    # Prevent pushing this gem to RubyGems.org. To allow pushes either set the 'allowed_push_host'
    # to allow pushing to a single host or delete this section to allow pushing to any host.
    if spec.respond_to?(:metadata)
        spec.metadata['allowed_push_host'] = "https://rubygems.org"
    else
        raise 'RubyGems 2.0 or newer is required to protect against public gem pushes.'
    end

    spec.files = `git ls-files -z`.split("\x0").reject do |f|
        f.match(%r{^(test|spec|features)/})
    end
    spec.bindir = 'exe'
    spec.executables = spec.files.grep(%r{^exe/}) { |f| File.basename(f) }
    spec.require_paths = ['lib']

    spec.add_dependency 'colorize', '~> 0.8'
    spec.add_dependency 'methadone', '~> 1.9'
    spec.add_dependency 'apex-aprs', '~> 1.0'
    spec.add_development_dependency 'bundler', '~> 1.7'
    spec.add_development_dependency 'rake', '~> 11.3'
    spec.add_development_dependency 'rdoc', '~> 4.2'
    spec.add_development_dependency 'aruba', '~> 0.14'
end
