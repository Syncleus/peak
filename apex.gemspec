# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'apex/version'

Gem::Specification.new do |spec|
  spec.name          = 'apex'
  spec.version       = Apex::VERSION
  spec.authors       = ['Jeffrey Phillips Freeman']
  spec.email         = ['jeffrey.freeman@syncleus.com']

  spec.summary       = %q{Reference implementation for the APEX Radio protocol.}
  spec.description   = %q{Reference implementation for the APEX Radio protocol.}
  spec.homepage      = 'http://apexprotocol.com'

  # Prevent pushing this gem to RubyGems.org. To allow pushes either set the 'allowed_push_host'
  # to allow pushing to a single host or delete this section to allow pushing to any host.
  if spec.respond_to?(:metadata)
    spec.metadata['allowed_push_host'] = "TODO: Set to 'http://mygemserver.com'"
  else
    raise 'RubyGems 2.0 or newer is required to protect against public gem pushes.'
  end

  spec.files         = `git ls-files -z`.split("\x0").reject do |f|
    f.match(%r{^(test|spec|features)/})
  end
  spec.bindir        = 'exe'
  spec.executables   = spec.files.grep(%r{^exe/}) { |f| File.basename(f) }
  spec.require_paths = ['lib']

  spec.add_development_dependency 'abstraction', '~> 0.0.4'
  spec.add_development_dependency 'json', '~> 1.8.3'
  spec.add_development_dependency 'bundler', '~> 1.13'
  spec.add_development_dependency 'rake', '~> 11.3.0'
  spec.add_development_dependency 'rdoc'
  spec.add_development_dependency 'aruba'
  spec.add_development_dependency 'serialport'
  spec.add_dependency 'methadone'
end
