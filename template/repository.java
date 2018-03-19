package {package}.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import {package}.{entityName};

public interface I{entityName}Repository extends JpaRepository<{entityName}, Long>
{
	
	@Query(value= "FROM {entityName} {entityNameLowerCamelCase} WHERE " +
			// {attributes}
	)
	public Page<{entityName}> listByFilters(@Param("filter") String filter, 
												   Pageable pageable);

}